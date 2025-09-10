import React from 'react';
import styled from 'styled-components';

const ErrorContainer = styled.div`
  background: #fed7d7;
  border: 1px solid #feb2b2;
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  margin: 20px 0;
`;

const ErrorIcon = styled.div`
  font-size: 48px;
  margin-bottom: 15px;
`;

const ErrorTitle = styled.h3`
  color: #c53030;
  font-size: 18px;
  margin: 0 0 10px 0;
`;

const ErrorText = styled.p`
  color: #742a2a;
  font-size: 14px;
  line-height: 1.5;
  margin: 0;
`;

function ErrorMessage({ message }) {
  return (
    <ErrorContainer>
      <ErrorIcon>⚠️</ErrorIcon>
      <ErrorTitle>エラーが発生しました</ErrorTitle>
      <ErrorText>{message}</ErrorText>
    </ErrorContainer>
  );
}

export default ErrorMessage;