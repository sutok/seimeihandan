import React, { useState } from 'react';
import styled from 'styled-components';
import NameInputForm from './components/NameInputForm';
import ResultDisplay from './components/ResultDisplay';
import Header from './components/Header';
import Footer from './components/Footer';
import LoadingSpinner from './components/LoadingSpinner';
import ErrorMessage from './components/ErrorMessage';
import './App.css';

// Styled Components
const AppContainer = styled.div`
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  flex-direction: column;
`;

const MainContent = styled.main`
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
  width: 100%;
`;

const ContentCard = styled.div`
  background: white;
  border-radius: 20px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  padding: 40px;
  margin: 20px;
  width: 100%;
  max-width: 600px;
  
  @media (max-width: 768px) {
    margin: 10px;
    padding: 20px;
    border-radius: 15px;
  }
`;

const ResetButton = styled.button`
  background: #6c7ae0;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 25px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  margin-top: 20px;
  transition: all 0.3s ease;
  
  &:hover {
    background: #5a67d8;
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(108, 122, 224, 0.3);
  }
  
  &:active {
    transform: translateY(0);
  }
`;

function App() {
  // State管理
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [submittedName, setSubmittedName] = useState(null);

  // API呼び出し処理
  const handleNameSubmit = async (lastName, firstName) => {
    setLoading(true);
    setError(null);
    setResult(null);
    
    try {
      // 本番環境用のAPI URL
      const apiUrl = process.env.REACT_APP_API_URL || 'https://seimei-handan-c4vnl29w.an.gateway.dev';
      
      const response = await fetch(`${apiUrl}/api/analyze`, {
        method: 'POST',
        mode: 'cors',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({
          lastName: lastName,
          firstName: firstName
        })
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      
      // バックエンドAPIのレスポンス処理
      if (data.success) {
        // 実際のAPIのレスポンス形式
        setResult(data.data);
        setSubmittedName({ lastName, firstName });
      } else {
        setError(data.error?.message || 'エラーが発生しました');
      }
    } catch (err) {
      console.error('API呼び出しエラー:', err);
      setError('サーバーとの通信に失敗しました。しばらく時間をおいて再度お試しください。');
    } finally {
      setLoading(false);
    }
  };

  // リセット処理
  const handleReset = () => {
    setResult(null);
    setError(null);
    setSubmittedName(null);
  };

  return (
    <AppContainer>
      <Header />
      
      <MainContent>
        <ContentCard>
          {/* 結果が無い場合：入力フォーム表示 */}
          {!result && !loading && (
            <NameInputForm onSubmit={handleNameSubmit} />
          )}
          
          {/* ローディング表示 */}
          {loading && <LoadingSpinner />}
          
          {/* エラー表示 */}
          {error && (
            <>
              <ErrorMessage message={error} />
              <ResetButton onClick={handleReset}>
                もう一度入力する
              </ResetButton>
            </>
          )}
          
          {/* 結果表示 */}
          {result && submittedName && (
            <>
              <ResultDisplay 
                result={result}
                lastName={submittedName.lastName}
                firstName={submittedName.firstName}
              />
              <ResetButton onClick={handleReset}>
                別の名前で診断する
              </ResetButton>
            </>
          )}
        </ContentCard>
      </MainContent>
      
      <Footer />
    </AppContainer>
  );
}

export default App;
