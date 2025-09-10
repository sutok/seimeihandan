import React from 'react';
import styled from 'styled-components';

const HeaderContainer = styled.header`
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  padding: 20px 0;
  text-align: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
`;

const Logo = styled.h1`
  color: white;
  font-size: 24px;
  font-weight: 700;
  margin: 0;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
  
  @media (max-width: 768px) {
    font-size: 20px;
  }
`;

function Header() {
  return (
    <HeaderContainer>
      <Logo>姓名判断アプリ</Logo>
    </HeaderContainer>
  );
}

export default Header;