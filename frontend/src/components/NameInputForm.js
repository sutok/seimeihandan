import React, { useState } from 'react';
import styled from 'styled-components';

// Styled Components
const FormContainer = styled.div`
  text-align: center;
`;

const Title = styled.h1`
  color: #2d3748;
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 10px;
  
  @media (max-width: 768px) {
    font-size: 24px;
  }
`;

const Subtitle = styled.p`
  color: #718096;
  font-size: 16px;
  margin-bottom: 40px;
  line-height: 1.6;
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
  gap: 30px;
`;

const InputGroup = styled.div`
  display: flex;
  align-items: center;
  gap: 20px;
  
  @media (max-width: 568px) {
    flex-direction: column;
    gap: 15px;
  }
`;

const Label = styled.label`
  font-size: 18px;
  font-weight: 600;
  color: #2d3748;
  min-width: 60px;
  
  @media (max-width: 568px) {
    min-width: auto;
  }
`;

const Input = styled.input`
  flex: 1;
  padding: 16px 20px;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 18px;
  font-weight: 500;
  transition: all 0.3s ease;
  background: #fafafa;
  
  &:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    background: white;
  }
  
  &::placeholder {
    color: #a0aec0;
    font-weight: 400;
  }
  
  @media (max-width: 568px) {
    width: 100%;
    font-size: 16px;
  }
`;

const CharCount = styled.span`
  font-size: 12px;
  color: #718096;
  margin-left: 10px;
  
  &.warning {
    color: #f56565;
  }
`;

const SubmitButton = styled.button`
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 18px 40px;
  border-radius: 30px;
  font-size: 18px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 20px;
  
  &:hover:not(:disabled) {
    transform: translateY(-3px);
    box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
  }
  
  &:active {
    transform: translateY(-1px);
  }
  
  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
  
  @media (max-width: 568px) {
    padding: 16px 32px;
    font-size: 16px;
  }
`;

const InfoText = styled.div`
  background: #f7fafc;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 20px;
  margin-top: 30px;
  color: #4a5568;
  font-size: 14px;
  line-height: 1.5;
`;

const InfoTitle = styled.h3`
  margin: 0 0 10px 0;
  color: #2d3748;
  font-size: 16px;
`;

const InfoList = styled.ul`
  margin: 0;
  padding-left: 20px;
  
  li {
    margin-bottom: 5px;
  }
`;

function NameInputForm({ onSubmit }) {
  const [lastName, setLastName] = useState('');
  const [firstName, setFirstName] = useState('');
  const [errors, setErrors] = useState({});

  // バリデーション処理
  const validateInput = (name, value) => {
    const newErrors = { ...errors };
    
    if (value.length > 10) {
      newErrors[name] = '10文字以内で入力してください';
    } else if (value.length === 0) {
      newErrors[name] = '必須項目です';
    } else {
      delete newErrors[name];
    }
    
    setErrors(newErrors);
  };

  // 入力値変更ハンドラー
  const handleLastNameChange = (e) => {
    const value = e.target.value;
    setLastName(value);
    validateInput('lastName', value);
  };

  const handleFirstNameChange = (e) => {
    const value = e.target.value;
    setFirstName(value);
    validateInput('firstName', value);
  };

  // フォーム送信ハンドラー
  const handleSubmit = (e) => {
    e.preventDefault();
    
    // 最終バリデーション
    const trimmedLastName = lastName.trim();
    const trimmedFirstName = firstName.trim();
    
    if (!trimmedLastName || !trimmedFirstName) {
      setErrors({
        lastName: !trimmedLastName ? '姓を入力してください' : '',
        firstName: !trimmedFirstName ? '名を入力してください' : ''
      });
      return;
    }
    
    if (trimmedLastName.length > 10 || trimmedFirstName.length > 10) {
      return;
    }
    
    // 親コンポーネントに送信
    onSubmit(trimmedLastName, trimmedFirstName);
  };

  // 送信ボタンの有効性
  const isSubmitDisabled = 
    !lastName.trim() || 
    !firstName.trim() || 
    Object.keys(errors).length > 0 ||
    lastName.length > 10 ||
    firstName.length > 10;

  return (
    <FormContainer>
      <Title>姓名判断</Title>
      <Subtitle>
        お名前を入力して、五格説による姓名判断を行います<br />
        漢字・ひらがなに対応しています
      </Subtitle>
      
      <Form onSubmit={handleSubmit}>
        <InputGroup>
          <Label htmlFor="lastName">姓</Label>
          <div style={{ flex: 1, display: 'flex', alignItems: 'center' }}>
            <Input
              id="lastName"
              type="text"
              value={lastName}
              onChange={handleLastNameChange}
              placeholder="田中"
              maxLength={15}
            />
            <CharCount className={lastName.length > 10 ? 'warning' : ''}>
              {lastName.length}/10
            </CharCount>
          </div>
        </InputGroup>
        
        {errors.lastName && (
          <div style={{ color: '#f56565', fontSize: '14px', textAlign: 'left' }}>
            {errors.lastName}
          </div>
        )}
        
        <InputGroup>
          <Label htmlFor="firstName">名</Label>
          <div style={{ flex: 1, display: 'flex', alignItems: 'center' }}>
            <Input
              id="firstName"
              type="text"
              value={firstName}
              onChange={handleFirstNameChange}
              placeholder="太郎"
              maxLength={15}
            />
            <CharCount className={firstName.length > 10 ? 'warning' : ''}>
              {firstName.length}/10
            </CharCount>
          </div>
        </InputGroup>
        
        {errors.firstName && (
          <div style={{ color: '#f56565', fontSize: '14px', textAlign: 'left' }}>
            {errors.firstName}
          </div>
        )}
        
        <SubmitButton type="submit" disabled={isSubmitDisabled}>
          診断する
        </SubmitButton>
      </Form>
      
      <InfoText>
        <InfoTitle>ご利用について</InfoTitle>
        <InfoList>
          <li>康熙字典準拠の画数で計算します</li>
          <li>五格説（天格・人格・地格・外格・総格）による判定</li>
          <li>漢字・ひらがなの混在入力が可能です</li>
          <li>一文字の姓名には霊数（+1画）を適用します</li>
        </InfoList>
      </InfoText>
    </FormContainer>
  );
}

export default NameInputForm;