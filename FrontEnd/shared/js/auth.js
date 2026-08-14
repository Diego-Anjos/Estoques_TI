/**
 * Sessão do usuário autenticado (login FastAPI + JWT).
 */
const USER_KEY = 'usuario';
const TOKEN_KEY = 'token';

/**
 * Persiste usuário e o JWT retornado pelo backend.
 * @param {{ id_usuario: number, nome: string, email: string, cargo?: string, access_token: string }} loginResponse
 */
export function saveSession(loginResponse) {
  if (!loginResponse?.access_token) {
    throw new Error('Login sem access_token — resposta inválida da API');
  }

  const usuario = {
    id_usuario: loginResponse.id_usuario,
    nome: loginResponse.nome,
    email: loginResponse.email,
    cargo: loginResponse.cargo ?? '',
  };
  localStorage.setItem(USER_KEY, JSON.stringify(usuario));
  localStorage.setItem(TOKEN_KEY, loginResponse.access_token);
  localStorage.removeItem('usuarioLogado');
  return usuario;
}

export function getSession() {
  try {
    const raw = localStorage.getItem(USER_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

/** Retorna o JWT armazenado (ou null). */
export function getAccessToken() {
  return localStorage.getItem(TOKEN_KEY);
}

export function clearSession() {
  localStorage.removeItem(USER_KEY);
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem('usuarioLogado');
}

export function isAuthenticated() {
  return Boolean(getSession() && getAccessToken());
}
