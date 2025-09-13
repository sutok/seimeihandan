import React from 'react';
import styled from 'styled-components';
import AffiliateBanner from './AffiliateBanner';

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
      <AffiliateBanner 
        title=""
        description="時間を節約したいなら、クラウドワークスAIが最適解。業務の自動化で、月に20時間の余裕が生まれる！その時間を趣味や学びに使おう。"
        buttonText="クラウドワークスAI"
        buttonUrl="https://ordermaid.ai/d/imzecwomvlqlfrbh"
      />
      <FooterText>
        © 2025 姓名判断アプリ | 康熙字典準拠・五格説
        <br />
        個人の娯楽目的でご利用ください
      </FooterText>
    </FooterContainer>
  );
}

export default Footer;