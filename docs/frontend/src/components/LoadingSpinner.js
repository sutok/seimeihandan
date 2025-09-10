import React from 'react';
import styled, { keyframes } from 'styled-components';

const spin = keyframes`
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
`;

const LoadingContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
`;

const Spinner = styled.div`
  width: 50px;
  height: 50px;
  border: 4px solid #e2e8f0;
  border-top: 4px solid #667eea;
  border-radius: 50%;
  animation: ${spin} 1s linear infinite;
  margin-bottom: 20px;
`;

const LoadingText = styled.p`
  color: #718096;
  font-size: 16px;
  margin: 0;
`;

function LoadingSpinner() {
  return (
    <LoadingContainer>
      <Spinner />
      <LoadingText>診断中...</LoadingText>
    </LoadingContainer>
  );
}

export default LoadingSpinner;