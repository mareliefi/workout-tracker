// frontend/src/contexts/AuthContext.js
import React, { createContext, useContext, useState, useEffect } from 'react';
import { authService } from '../services/authService';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user data exists in localStorage
    const savedUser = localStorage.getItem('user');
    if (savedUser) {
      setUser(JSON.parse(savedUser));
    }
    setLoading(false);
  }, []);

  const login = async (email, password) => {
    setLoading(true);
    const result = await authService.login(email, password);
    
    if (result.success) {
      const userData = { email }; // You might want to fetch more user data
      setUser(userData);
      localStorage.setItem('user', JSON.stringify(userData));
    }
    
    setLoading(false);
    return result;
  };

  const register = async (userData) => {
    setLoading(true);
    const result = await authService.register(userData);
    setLoading(false);
    return result;
  };

  const logout = async () => {
    setLoading(true);
    await authService.logout();
    setUser(null);
    localStorage.removeItem('user');
    setLoading(false);
  };

  const value = {
    user,
    login,
    register,
    logout,
    loading,
    isAuthenticated: !!user,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};