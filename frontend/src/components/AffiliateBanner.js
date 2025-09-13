import React from 'react';
import styled from 'styled-components';

// Styled Components
const AffiliateContainer = styled.div`
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  padding: 20px;
  margin: 20px 0;
  text-align: center;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2);
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
  }
`;

const AffiliateTitle = styled.h3`
  color: white;
  font-size: 18px;
  font-weight: 700;
  margin: 0 0 15px 0;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
`;

const AffiliateDescription = styled.p`
  color: rgba(255, 255, 255, 0.9);
  font-size: 14px;
  margin: 0 0 15px 0;
  line-height: 1.5;
`;

const AffiliateButton = styled.a`
  display: inline-block;
  background: white;
  color: #667eea;
  padding: 12px 24px;
  border-radius: 25px;
  text-decoration: none;
  font-weight: 600;
  font-size: 16px;
  transition: all 0.3s ease;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  
  &:hover {
    background: #f7fafc;
    transform: translateY(-1px);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
    color: #5a67d8;
  }
  
  &:active {
    transform: translateY(0);
  }
`;

const AffiliateImage = styled.img`
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  margin: 10px 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
`;

function AffiliateBanner({ 
  title = "おすすめサービス", 
  description = "あなたの運勢をさらに詳しく知りたい方におすすめのサービスです。",
  buttonText = "詳細を見る",
  buttonUrl = "#",
  imageUrl = null,
  imageAlt = "おすすめサービス"
}) {
  return (
    <AffiliateContainer>
      <AffiliateTitle>{title}</AffiliateTitle>
      <AffiliateDescription>{description}</AffiliateDescription>
      
      {imageUrl && (
        <AffiliateImage 
          src={imageUrl} 
          alt={imageAlt}
          onError={(e) => {
            e.target.style.display = 'none';
          }}
        />
      )}
      
      <AffiliateButton 
        href={buttonUrl} 
        target="_blank" 
        rel="noopener noreferrer"
      >
        {buttonText}
      </AffiliateButton>
    </AffiliateContainer>
  );
}

export default AffiliateBanner;
