import React, { createContext, useContext, useEffect, useState } from 'react';
import type { ReactNode } from 'react';
import { createOrGetUser } from '../services/UserApi';
import type { User } from '../services/UserApi';

interface UserContextType {
  user: User | null;
  setUser: (user: User | null) => void;
  login: (userName: string) => Promise<void>;
  logout: () => void;
  isLoading: boolean;
}

const UserContext = createContext<UserContextType | undefined>(undefined);

export const UserProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // При монтировании пытаемся загрузить пользователя из localStorage
  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      try {
        setUser(JSON.parse(storedUser));
      } catch (e) {
        localStorage.removeItem('user');
      }
    }
    setIsLoading(false);
  }, []);

  const login = async (userName: string) => {
    setIsLoading(true);
    try {
      const user = await createOrGetUser(userName);
      setUser(user);
      localStorage.setItem('user', JSON.stringify(user));
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('user');
  };

  return (
    <UserContext.Provider value={{ user, setUser, login, logout, isLoading }}>
      {children}
    </UserContext.Provider>
  );
};

export const useUser = () => {
  const context = useContext(UserContext);
  if (context === undefined) {
    throw new Error('useUser must be used within a UserProvider');
  }
  return context;
};