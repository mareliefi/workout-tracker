// frontend/src/services/authService.js
import api from '../config/api';

export const authService = {
  async login(email, password) {
    try {
      const response = await api.post('/auth/login', {
        email,
        password,
      });
      return { success: true, data: response.data };
    } catch (error) {
      return {
        success: false,
        message: error.response?.data?.message || 'Login failed',
      };
    }
  },

  async register(userData) {
    try {
      const response = await api.post('/auth/signup', userData);
      return { success: true, data: response.data };
    } catch (error) {
      return {
        success: false,
        message: error.response?.data?.message || 'Registration failed',
      };
    }
  },

  async logout() {
    try {
      await api.post('/auth/logout');
      localStorage.removeItem('user');
      return { success: true };
    } catch (error) {
      return {
        success: false,
        message: error.response?.data?.message || 'Logout failed',
      };
    }
  },
};