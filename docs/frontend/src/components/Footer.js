import React from 'react';
import styled from 'styled-components';

const FooterContainer = styled.footer`
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  padding: 20px;
  text-align: center;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  margin-top: auto;
`;

const FooterText = styled.p`
  color: rgba(255, 255, 255, 0.8);
  font-size: 14px;
  margin: 0;
  line-height: 1.5;
`;

function Footer() {
  return (
    <FooterContainer>
      <FooterText>
        © 2025 姓名判断アプリ | 康熙字典準拠・五格説
        <br />
        個人の娯楽目的でご利用ください
      </FooterText>
    </FooterContainer>
  );
}

export default Footer;