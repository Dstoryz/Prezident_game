import React, { useState } from 'react';

const DebugAuth: React.FC = () => {
  const [formData, setFormData] = useState({
    email: '',
    username: '',
    password: '',
    password_confirm: '',
    first_name: '',
    last_name: '',
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [debugInfo, setDebugInfo] = useState('');
  const [isLogin, setIsLogin] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setDebugInfo('');
    setIsLoading(true);

    try {
      const url = isLogin 
        ? 'http://localhost:8000/api/auth/login/'
        : 'http://localhost:8000/api/auth/register/';
      
      const body = isLogin 
        ? { email: formData.email, password: formData.password }
        : formData;

      setDebugInfo(`Отправляем запрос на: ${url}\nДанные: ${JSON.stringify(body, null, 2)}`);

      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(body),
      });

      setDebugInfo(prev => prev + `\n\nСтатус ответа: ${response.status} ${response.statusText}`);

      const responseText = await response.text();
      setDebugInfo(prev => prev + `\n\nОтвет сервера: ${responseText}`);

      if (response.ok) {
        const data = JSON.parse(responseText);
        setSuccess(`Успешно! ${isLogin ? 'Вход' : 'Регистрация'} выполнен.`);
        setDebugInfo(prev => prev + `\n\nТокены получены: ${data.tokens ? 'Да' : 'Нет'}`);
      } else {
        setError(`Ошибка ${response.status}: ${responseText}`);
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : String(err);
      setError(`Ошибка сети: ${errorMessage}`);
      setDebugInfo(prev => prev + `\n\nОшибка: ${errorMessage}`);
    }
    
    setIsLoading(false);
  };

  return (
    <div style={{ 
      padding: '20px', 
      maxWidth: '800px', 
      margin: '0 auto',
      fontFamily: 'Arial, sans-serif'
    }}>
      <h2 style={{ textAlign: 'center', color: '#333' }}>
        Отладка {isLogin ? 'входа' : 'регистрации'}
      </h2>
      
      {error && (
        <div style={{ 
          color: 'red', 
          marginBottom: '10px', 
          padding: '10px',
          backgroundColor: '#ffe6e6',
          borderRadius: '5px',
          border: '1px solid #ff9999'
        }}>
          {error}
        </div>
      )}
      
      {success && (
        <div style={{ 
          color: 'green', 
          marginBottom: '10px', 
          padding: '10px',
          backgroundColor: '#e6ffe6',
          borderRadius: '5px',
          border: '1px solid #99ff99'
        }}>
          {success}
        </div>
      )}
      
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '15px' }}>
          <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>
            Email: *
          </label>
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
            style={{ 
              width: '100%', 
              padding: '10px', 
              border: '1px solid #ddd',
              borderRadius: '5px',
              fontSize: '16px'
            }}
          />
        </div>
        
        {!isLogin && (
          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>
              Имя пользователя: *
            </label>
            <input
              type="text"
              name="username"
              value={formData.username}
              onChange={handleChange}
              required
              style={{ 
                width: '100%', 
                padding: '10px', 
                border: '1px solid #ddd',
                borderRadius: '5px',
                fontSize: '16px'
              }}
            />
          </div>
        )}
        
        <div style={{ marginBottom: '15px' }}>
          <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>
            Пароль: *
          </label>
          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
            style={{ 
              width: '100%', 
              padding: '10px', 
              border: '1px solid #ddd',
              borderRadius: '5px',
              fontSize: '16px'
            }}
          />
        </div>
        
        {!isLogin && (
          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>
              Подтвердите пароль: *
            </label>
            <input
              type="password"
              name="password_confirm"
              value={formData.password_confirm}
              onChange={handleChange}
              required
              style={{ 
                width: '100%', 
                padding: '10px', 
                border: '1px solid #ddd',
                borderRadius: '5px',
                fontSize: '16px'
              }}
            />
          </div>
        )}
        
        {!isLogin && (
          <>
            <div style={{ marginBottom: '15px' }}>
              <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>
                Имя:
              </label>
              <input
                type="text"
                name="first_name"
                value={formData.first_name}
                onChange={handleChange}
                style={{ 
                  width: '100%', 
                  padding: '10px', 
                  border: '1px solid #ddd',
                  borderRadius: '5px',
                  fontSize: '16px'
                }}
              />
            </div>
            
            <div style={{ marginBottom: '15px' }}>
              <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>
                Фамилия:
              </label>
              <input
                type="text"
                name="last_name"
                value={formData.last_name}
                onChange={handleChange}
                style={{ 
                  width: '100%', 
                  padding: '10px', 
                  border: '1px solid #ddd',
                  borderRadius: '5px',
                  fontSize: '16px'
                }}
              />
            </div>
          </>
        )}
        
        <div style={{ display: 'flex', gap: '10px', marginBottom: '15px' }}>
          <button 
            type="submit"
            disabled={isLoading}
            style={{ 
              flex: 1,
              padding: '12px 20px', 
              backgroundColor: '#007bff', 
              color: 'white', 
              border: 'none', 
              borderRadius: '5px',
              fontSize: '16px',
              cursor: isLoading ? 'not-allowed' : 'pointer',
              opacity: isLoading ? 0.6 : 1
            }}
          >
            {isLoading ? 'Обработка...' : (isLogin ? 'Войти' : 'Зарегистрироваться')}
          </button>
        </div>
      </form>
      
      <div style={{ textAlign: 'center', marginBottom: '20px' }}>
        <button 
          type="button"
          onClick={() => {
            setIsLogin(!isLogin);
            setError('');
            setSuccess('');
            setDebugInfo('');
          }}
          style={{ 
            background: 'none',
            border: 'none',
            color: '#007bff',
            textDecoration: 'underline',
            cursor: 'pointer',
            fontSize: '14px'
          }}
        >
          {isLogin ? 'Создать аккаунт' : 'Уже есть аккаунт? Войти'}
        </button>
      </div>

      {debugInfo && (
        <div style={{ 
          marginTop: '20px',
          padding: '15px',
          backgroundColor: '#f8f9fa',
          border: '1px solid #dee2e6',
          borderRadius: '5px',
          fontFamily: 'monospace',
          fontSize: '12px',
          whiteSpace: 'pre-wrap',
          maxHeight: '400px',
          overflow: 'auto'
        }}>
          <strong>Отладочная информация:</strong>
          {debugInfo}
        </div>
      )}
    </div>
  );
};

export default DebugAuth; 