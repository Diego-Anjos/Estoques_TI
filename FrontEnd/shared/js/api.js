/**
 * Cliente HTTP compartilhado para a API FastAPI.
 * Uso: import { api } from '../../../shared/js/api.js';
 */
import { API_URL } from './config.js';

/**
 * @param {string} path - Caminho relativo (ex: "/usuarios/login")
 * @param {RequestInit & { json?: unknown }} [options]
 * @returns {Promise<any>}
 */
export async function apiRequest(path, options = {}) {
  const { json, headers: customHeaders, ...rest } = options;
  const headers = new Headers(customHeaders || {});

  if (json !== undefined && !headers.has('Content-Type')) {
    headers.set('Content-Type', 'application/json');
  }

  const token = localStorage.getItem('token');
  if (token && !headers.has('Authorization')) {
    headers.set('Authorization', `Bearer ${token}`);
  }

  const url = `${API_URL}/${String(path).replace(/^\//, '')}`;
  const response = await fetch(url, {
    ...rest,
    headers,
    body: json !== undefined ? JSON.stringify(json) : rest.body,
  });

  const contentType = response.headers.get('content-type') || '';
  const payload = contentType.includes('application/json')
    ? await response.json()
    : await response.text();

  if (!response.ok) {
    let detail =
      typeof payload === 'object' && payload !== null
        ? payload.detail ?? payload.message ?? payload
        : payload || response.statusText;

    if (Array.isArray(detail)) {
      detail = detail
        .map((item) => (typeof item === 'object' ? item.msg || JSON.stringify(item) : String(item)))
        .join('\n');
    } else if (detail && typeof detail === 'object') {
      detail = JSON.stringify(detail);
    }

    const error = new Error(typeof detail === 'string' ? detail : 'Erro na API');
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
  const headers = new Headers();
  const token = localStorage.getItem('token');
  if (token) headers.set('Authorization', `Bearer ${token}`);

  const url = `${API_URL}/${String(path).replace(/^\//, '')}`;
  const response = await fetch(url, { method: 'GET', headers });

  if (!response.ok) {
    let detail = response.statusText;
    try {
      const payload = await response.json();
      detail = payload.detail || payload.message || detail;
      if (Array.isArray(detail)) {
        detail = detail.map((i) => i.msg || String(i)).join('\n');
      }
    } catch {
      /* ignore */
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
