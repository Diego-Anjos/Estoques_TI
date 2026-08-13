/**
 * Sessão do usuário autenticado (login FastAPI).
 * A API atual não emite JWT; guardamos os dados do login para a sessão.
 */
const USER_KEY = 'usuario';
const TOKEN_KEY = 'token';

export function saveSession(loginResponse) {
  const usuario = {
    id_usuario: loginResponse.id_usuario,
    nome: loginResponse.nome,
    email: loginResponse.email,
    cargo: loginResponse.cargo ?? '',
  };
  localStorage.setItem(USER_KEY, JSON.stringify(usuario));
  // Marcador de sessão até existir JWT de verdade
  localStorage.setItem(TOKEN_KEY, `session:${usuario.id_usuario}`);
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

export function clearSession() {
  localStorage.removeItem(USER_KEY);
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem('usuarioLogado');
}

export function isAuthenticated() {
  return Boolean(getSession() && localStorage.getItem(TOKEN_KEY));
}
