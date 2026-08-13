/**
 * ========================================
 * UTILITÁRIOS JAVASCRIPT - SISTEMA CONTROLE DE ESTOQUE
 * ========================================
 */

// Utilitários de formatação
export const formatUtils = {
  /**
   * Formata data para padrão brasileiro
   * @param {Date|string} date - Data para formatar
   * @returns {string} Data formatada (DD/MM/AAAA)
   */
  formatDate(date) {
    if (!date) return '';
    const dateObj = new Date(date);
    return dateObj.toLocaleDateString('pt-BR');
  },

  /**
   * Formata data e hora para padrão brasileiro
   * @param {Date|string} date - Data para formatar
   * @returns {string} Data e hora formatadas (DD/MM/AAAA HH:mm)
   */
  formatDateTime(date) {
    if (!date) return '';
    const dateObj = new Date(date);
    return dateObj.toLocaleString('pt-BR');
  },

  /**
   * Formata número para moeda brasileira
   * @param {number} value - Valor para formatar
   * @returns {string} Valor formatado (R$ 0,00)
   */
  formatCurrency(value) {
    if (isNaN(value)) return 'R$ 0,00';
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value);
  },

  /**
   * Formata número com separadores de milhares
   * @param {number} value - Valor para formatar
   * @returns {string} Número formatado
   */
  formatNumber(value) {
    if (isNaN(value)) return '0';
    return new Intl.NumberFormat('pt-BR').format(value);
  }
};

// Utilitários de validação
export const validationUtils = {
  /**
   * Valida se o email é válido
   * @param {string} email - Email para validar
   * @returns {boolean} True se válido
   */
  isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  },

  /**
   * Valida se a string não está vazia
   * @param {string} value - Valor para validar
   * @returns {boolean} True se não está vazio
   */
  isNotEmpty(value) {
    return value && value.trim().length > 0;
  },

  /**
   * Valida se o número está dentro do range
   * @param {number} value - Valor para validar
   * @param {number} min - Valor mínimo
   * @param {number} max - Valor máximo
   * @returns {boolean} True se válido
   */
  isInRange(value, min, max) {
    return value >= min && value <= max;
  },

  /**
   * Valida se o campo obrigatório foi preenchido
   * @param {any} value - Valor para validar
   * @returns {boolean} True se válido
   */
  isRequired(value) {
    if (typeof value === 'string') {
      return this.isNotEmpty(value);
    }
    return value !== null && value !== undefined;
  }
};

// Utilitários de DOM
export const domUtils = {
  /**
   * Seleciona elemento do DOM
   * @param {string} selector - Seletor CSS
   * @returns {Element|null} Elemento encontrado
   */
  $(selector) {
    return document.querySelector(selector);
  },

  /**
   * Seleciona múltiplos elementos do DOM
   * @param {string} selector - Seletor CSS
   * @returns {NodeList} Lista de elementos
   */
  $$(selector) {
    return document.querySelectorAll(selector);
  },

  /**
   * Adiciona classe a um elemento
   * @param {Element} element - Elemento
   * @param {string} className - Nome da classe
   */
  addClass(element, className) {
    if (element) {
      element.classList.add(className);
    }
  },

  /**
   * Remove classe de um elemento
   * @param {Element} element - Elemento
   * @param {string} className - Nome da classe
   */
  removeClass(element, className) {
    if (element) {
      element.classList.remove(className);
    }
  },

  /**
   * Alterna classe em um elemento
   * @param {Element} element - Elemento
   * @param {string} className - Nome da classe
   */
  toggleClass(element, className) {
    if (element) {
      element.classList.toggle(className);
    }
  },

  /**
   * Mostra elemento
   * @param {Element} element - Elemento
   */
  show(element) {
    if (element) {
      element.style.display = 'block';
    }
  },

  /**
   * Esconde elemento
   * @param {Element} element - Elemento
   */
  hide(element) {
    if (element) {
      element.style.display = 'none';
    }
  }
};

// Utilitários de debounce/throttle
export const timingUtils = {
  /**
   * Debounce - executa função após delay sem novas chamadas
   * @param {Function} func - Função para executar
   * @param {number} delay - Delay em ms
   * @returns {Function} Função com debounce
   */
  debounce(func, delay) {
    let timeoutId;
    return function (...args) {
      clearTimeout(timeoutId);
      timeoutId = setTimeout(() => func.apply(this, args), delay);
    };
  },

  /**
   * Throttle - executa função no máximo uma vez por período
   * @param {Function} func - Função para executar
   * @param {number} limit - Limite em ms
   * @returns {Function} Função com throttle
   */
  throttle(func, limit) {
    let inThrottle;
    return function (...args) {
      if (!inThrottle) {
        func.apply(this, args);
        inThrottle = true;
        setTimeout(() => inThrottle = false, limit);
      }
    };
  }
};

// Utilitários de armazenamento
export const storageUtils = {
  /**
   * Salva item no localStorage
   * @param {string} key - Chave
   * @param {any} value - Valor
   */
  set(key, value) {
    try {
      localStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
      console.error('Erro ao salvar no localStorage:', error);
    }
  },

  /**
   * Recupera item do localStorage
   * @param {string} key - Chave
   * @returns {any} Valor recuperado
   */
  get(key) {
    try {
      const item = localStorage.getItem(key);
      return item ? JSON.parse(item) : null;
    } catch (error) {
      console.error('Erro ao recuperar do localStorage:', error);
      return null;
    }
  },

  /**
   * Remove item do localStorage
   * @param {string} key - Chave
   */
  remove(key) {
    try {
      localStorage.removeItem(key);
    } catch (error) {
      console.error('Erro ao remover do localStorage:', error);
    }
  },

  /**
   * Limpa todo o localStorage
   */
  clear() {
    try {
      localStorage.clear();
    } catch (error) {
      console.error('Erro ao limpar localStorage:', error);
    }
  }
};

// Utilitários de loading
export const loadingUtils = {
  /**
   * Mostra loading em elemento
   * @param {Element} element - Elemento
   * @param {string} text - Texto do loading
   */
  show(element, text = 'Carregando...') {
    if (!element) return;
    
    element.innerHTML = `
      <div class="loading-container">
        <div class="loading-spinner"></div>
        <span class="loading-text">${text}</span>
      </div>
    `;
    element.style.display = 'flex';
    element.style.alignItems = 'center';
    element.style.justifyContent = 'center';
    element.style.gap = '8px';
  },

  /**
   * Esconde loading
   * @param {Element} element - Elemento
   */
  hide(element) {
    if (!element) return;
    element.innerHTML = '';
    element.style.display = '';
  }
};

// Utilitários de notificação
export const notificationUtils = {
  /**
   * Mostra notificação de sucesso
   * @param {string} message - Mensagem
   */
  success(message) {
    this.show(message, 'success');
  },

  /**
   * Mostra notificação de erro
   * @param {string} message - Mensagem
   */
  error(message) {
    this.show(message, 'error');
  },

  /**
   * Mostra notificação de aviso
   * @param {string} message - Mensagem
   */
  warning(message) {
    this.show(message, 'warning');
  },

  /**
   * Mostra notificação de informação
   * @param {string} message - Mensagem
   */
  info(message) {
    this.show(message, 'info');
  },

  /**
   * Mostra notificação
   * @param {string} message - Mensagem
   * @param {string} type - Tipo da notificação
   */
  show(message, type = 'info') {
    // Implementação básica - pode ser melhorada com toast library
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Adiciona estilo básico
    notification.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      padding: 12px 20px;
      border-radius: 6px;
      color: white;
      font-weight: 500;
      z-index: 9999;
      animation: slideIn 0.3s ease;
    `;
    
    // Define cor baseada no tipo
    const colors = {
      success: '#10b981',
      error: '#ef4444',
      warning: '#f59e0b',
      info: '#06b6d4'
    };
    
    notification.style.backgroundColor = colors[type] || colors.info;
    
    document.body.appendChild(notification);
    
    // Remove após 5 segundos
    setTimeout(() => {
      if (notification.parentNode) {
        notification.remove();
      }
    }, 5000);
  }
};