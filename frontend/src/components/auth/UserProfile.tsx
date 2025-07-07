import React, { useState, useEffect, useRef } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import './UserProfile.css';

const UserProfile: React.FC = () => {
  const { user, logout } = useAuth();
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Закрытие dropdown при клике вне его
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsDropdownOpen(false);
      }
    };

    if (isDropdownOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isDropdownOpen]);

  if (!user) {
    return null;
  }

  const handleLogout = () => {
    logout();
    setIsDropdownOpen(false);
  };

  const toggleDropdown = () => {
    setIsDropdownOpen(!isDropdownOpen);
  };

  return (
    <div className="user-profile" ref={dropdownRef}>
      <div className="user-avatar" onClick={toggleDropdown}>
        <span>{user.first_name?.[0] || user.username?.[0] || user.email?.[0] || '?'}</span>
      </div>
      
      {isDropdownOpen && (
        <div className="user-dropdown">
          <div className="user-info">
            <div className="user-name">
              {user.first_name && user.last_name 
                ? `${user.first_name} ${user.last_name}`
                : user.username || user.email || 'Пользователь'
              }
            </div>
            <div className="user-email">{user.email}</div>
            <div className="user-stats">
              <span>Игр сыграно: {user.games_played}</span>
              <span>Лучший счет: {user.best_score}</span>
            </div>
          </div>
          
          <div className="user-actions">
            <button className="logout-btn" onClick={handleLogout}>
              Выйти
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default UserProfile; 