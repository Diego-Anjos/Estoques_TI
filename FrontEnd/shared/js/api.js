/**
 * Cliente HTTP compartilhado para a API FastAPI.
 * Injeta automaticamente Authorization: Bearer <JWT> em todas as requisições.
 * Uso: import { api } from '../../../shared/js/api.js';
 */
import { API_URL } from './config.js';
import { getAccessToken, clearSession } from './auth.js';
import { showNotification } from './notify.js';

const OFFLINE_MESSAGE =
  'Erro de conexão: O servidor da API não está respondendo. Verifique se o Backend está ativo na porta 8000.';

/** Evita spam de toasts quando várias requisições falham juntas (API offline). */
let lastOfflineNotifyAt = 0;
const OFFLINE_NOTIFY_COOLDOWN_MS = 4000;

/**
 * Monta headers com Content-Type (quando há JSON) e Bearer token.
 * @param {HeadersInit} [customHeaders]
 * @param {{ json?: boolean, skipAuth?: boolean }} [opts]
 */
function buildHeaders(customHeaders, opts = {}) {
  const headers = new Headers(customHeaders || {});

  if (opts.json && !headers.has('Content-Type')) {
    headers.set('Content-Type', 'application/json');
  }

  // Rotas públicas (login/registro) não devem enviar JWT antigo/inválido
  if (!opts.skipAuth) {
    const token = getAccessToken();
    if (token && !headers.has('Authorization')) {
      headers.set('Authorization', `Bearer ${token}`);
    }
  }

  return headers;
}

/**
 * Detecta falha típica de servidor offline / conexão recusada
 * (ERR_CONNECTION_REFUSED → "Failed to fetch" / NetworkError).
 * @param {unknown} error
 * @param {Response} [response]
 */
function isNetworkError(error, response) {
  if (response && typeof response.status === 'number') return false;
  if (response === undefined && error && typeof error === 'object' && 'status' in error) {
    // Erros de API já tipados não são de rede
    if (typeof error.status === 'number') return false;
  }

  const message = String(error?.message ?? error ?? '');
  const name = String(error?.name ?? '');
  return (
    /failed to fetch|networkerror|network request failed|load failed|err_connection_refused/i.test(
      message
    ) ||
    /networkerror/i.test(name) ||
    (error instanceof TypeError && /fetch/i.test(message))
  );
}

/**
 * Notifica o usuário e lança erro amigável quando a API está offline.
 * @param {unknown} cause
 * @returns {never}
 */
function throwOfflineError(cause) {
  const now = Date.now();
  if (now - lastOfflineNotifyAt > OFFLINE_NOTIFY_COOLDOWN_MS) {
    lastOfflineNotifyAt = now;
    showNotification(OFFLINE_MESSAGE, 'error');
  }

  const error = new Error(OFFLINE_MESSAGE);
  error.isNetworkError = true;
  error.notified = true;
  error.cause = cause;
  throw error;
}

/** Resolve a URL da tela de login a partir de qualquer profundidade em /pages/. */
function resolveLoginUrl() {
  const path = window.location.pathname;
  const pagesIdx = path.indexOf('/pages/');
  if (pagesIdx !== -1) {
    return `${path.slice(0, pagesIdx)}/pages/auth/login/index.html`;
  }
  // Fallback relativo (páginas sob pages/)
  return new URL('../auth/login/index.html', window.location.href).href;
}

/**
 * Sessão inválida/expirada: limpa storage e redireciona para login
 * (evita tela "fantasma" após 401/403 de autenticação).
 */
function forceReauthentication() {
  clearSession();
  if (/\/auth\/login\//i.test(window.location.pathname)) {
    return; // já está no login — evita loop/reload
  }
  window.location.href = resolveLoginUrl();
}

/**
 * 401 sempre; 403 quando a request não tinha Authorization
 * (FastAPI HTTPBearer → "Not authenticated") ou usuário inativo.
 * @param {number} status
 * @param {Headers} requestHeaders
 * @param {unknown} detail
 */
function shouldForceLogin(status, requestHeaders, detail) {
  if (status === 401) return true;
  if (status !== 403) return false;

  const hadAuthorization = requestHeaders.has('Authorization');
  if (!hadAuthorization) return true;

  const text = typeof detail === 'string' ? detail : JSON.stringify(detail ?? '');
  return /not authenticated|usu[áa]rio inativo/i.test(text);
}

/**
 * Extrai mensagem amigável do body FastAPI (detail string | array 422).
 * @param {any} payload
 * @param {string} fallback
 */
function extractDetail(payload, fallback) {
  let detail =
    typeof payload === 'object' && payload !== null
      ? payload.detail ?? payload.message ?? payload
      : payload || fallback;

  if (Array.isArray(detail)) {
    detail = detail
      .map((item) => (typeof item === 'object' ? item.msg || JSON.stringify(item) : String(item)))
      .join('\n');
  } else if (detail && typeof detail === 'object') {
    detail = JSON.stringify(detail);
  }

  return typeof detail === 'string' ? detail : fallback;
}

/**
 * @param {string} path - Caminho relativo (ex: "/usuarios/login")
 * @param {RequestInit & { json?: unknown, skipAuth?: boolean }} [options]
 * @returns {Promise<any>}
 */
export async function apiRequest(path, options = {}) {
  const { json, headers: customHeaders, skipAuth = false, ...rest } = options;
  const headers = buildHeaders(customHeaders, {
    json: json !== undefined,
    skipAuth,
  });

  const url = `${API_URL}/${String(path).replace(/^\//, '')}`;
  let response;

  try {
    response = await fetch(url, {
      ...rest,
      headers,
      body: json !== undefined ? JSON.stringify(json) : rest.body,
    });
  } catch (error) {
    if (isNetworkError(error, response)) {
      throwOfflineError(error);
    }
    throw error;
  }

  // Sem status → trata como falha de rede (defesa extra)
  if (response == null || typeof response.status !== 'number') {
    throwOfflineError(response);
  }

  const contentType = response.headers.get('content-type') || '';
  const payload = contentType.includes('application/json')
    ? await response.json()
    : await response.text();

  if (!response.ok) {
    const detail = extractDetail(payload, response.statusText);

    if (shouldForceLogin(response.status, headers, detail)) {
      forceReauthentication();
    }

    const error = new Error(detail || 'Erro na API');
    error.status = response.status;
    error.payload = payload;
    throw error;
  }

  return payload;
}

export const api = {
  get: (path, options) => apiRequest(path, { ...options, method: 'GET' }),
  post: (path, json, options) => apiRequest(path, { ...options, method: 'POST', json }),
  put: (path, json, options) => apiRequest(path, { ...options, method: 'PUT', json }),
  patch: (path, json, options) => apiRequest(path, { ...options, method: 'PATCH', json }),
  delete: (path, options) => apiRequest(path, { ...options, method: 'DELETE' }),
};

/**
 * Baixa um arquivo binário/texto da API (ex.: CSV).
 * @param {string} path
 * @param {string} [fallbackFilename]
 */
export async function apiDownload(path, fallbackFilename = 'download.csv') {
  const headers = buildHeaders();

  const url = `${API_URL}/${String(path).replace(/^\//, '')}`;
  let response;

  try {
    response = await fetch(url, { method: 'GET', headers });
  } catch (error) {
    if (isNetworkError(error, response)) {
      throwOfflineError(error);
    }
    throw error;
  }

  if (response == null || typeof response.status !== 'number') {
    throwOfflineError(response);
  }

  if (!response.ok) {
    let detail = response.statusText;
    try {
      const payload = await response.json();
      detail = extractDetail(payload, detail);
    } catch {
      /* ignore */
    }

    if (shouldForceLogin(response.status, headers, detail)) {
      forceReauthentication();
    }

    throw new Error(typeof detail === 'string' ? detail : 'Falha no download');
  }

  const disposition = response.headers.get('Content-Disposition') || '';
  const match = /filename="?([^"]+)"?/i.exec(disposition);
  const filename = match?.[1] || fallbackFilename;
  const blob = await response.blob();
  const objectUrl = URL.createObjectURL(blob);
  const anchor = document.createElement('a');
  anchor.href = objectUrl;
  anchor.download = filename;
  document.body.appendChild(anchor);
  anchor.click();
  anchor.remove();
  URL.revokeObjectURL(objectUrl);
}

export { API_URL };
