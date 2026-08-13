/**
 * Configuração central do frontend.
 * A URL da API vem de VITE_API_URL (.env) — nunca hardcode a base nas páginas.
 */
const DEFAULT_API_URL = 'http://localhost:8000/api';

export const API_URL = (
  (typeof import.meta !== 'undefined' && import.meta.env?.VITE_API_URL) ||
  DEFAULT_API_URL
).replace(/\/$/, '');
