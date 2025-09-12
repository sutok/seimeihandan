import React from 'react';
import styled from 'styled-components';

// Styled Components
const ResultContainer = styled.div`
  text-align: center;
`;

const NameTitle = styled.h1`
  color: #2d3748;
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 10px;
  
  @media (max-width: 768px) {
    font-size: 24px;
  }
`;

const OverallResult = styled.div`
  background: ${props => getResultColor(props.result)};
  color: white;
  padding: 20px;
  border-radius: 15px;
  margin: 20px 0 30px 0;
  font-size: 24px;
  font-weight: 700;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
  
  @media (max-width: 768px) {
    font-size: 20px;
    padding: 15px;
  }
`;

const CharacterSection = styled.div`
  background: #f7fafc;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 30px;
`;

const CharacterTitle = styled.h3`
  color: #2d3748;
  font-size: 18px;
  margin-bottom: 15px;
`;

const CharacterGrid = styled.div`
  display: flex;
  justify-content: center;
  gap: 15px;
  flex-wrap: wrap;
`;

const CharacterCard = styled.div`
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 10px;
  padding: 15px;
  min-width: 80px;
  text-align: center;
  
  .character {
    font-size: 24px;
    font-weight: 700;
    color: #2d3748;
    margin-bottom: 5px;
  }
  
  .stroke {
    font-size: 14px;
    color: #718096;
  }
`;

const GogakuSection = styled.div`
  margin-top: 30px;
`;

const GogakuTitle = styled.h3`
  color: #2d3748;
  font-size: 20px;
  margin-bottom: 20px;
`;

const GogakuGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
  
  @media (max-width: 768px) {
    grid-template-columns: 1fr;
    gap: 15px;
  }
`;

const GogakuCard = styled.div`
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  padding: 20px;
  text-align: left;
  transition: all 0.3s ease;
  
  &:hover {
    border-color: #667eea;
    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.1);
  }
`;

const KakuName = styled.h4`
  color: #2d3748;
  font-size: 16px;
  margin: 0 0 10px 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const KakuValue = styled.span`
  background: #667eea;
  color: white;
  padding: 4px 12px;
  border-radius: 15px;
  font-size: 14px;
  font-weight: 600;
`;

const KakuResult = styled.div`
  background: ${props => getResultColor(props.result)};
  color: white;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 600;
  display: inline-block;
  margin-bottom: 10px;
`;

const KakuDescription = styled.p`
  color: #4a5568;
  font-size: 14px;
  line-height: 1.5;
  margin: 0;
`;

// 結果に応じた色を返す関数
function getResultColor(result) {
  switch (result) {
    case '大吉':
      return 'linear-gradient(135deg, #48bb78, #38a169)';
    case '吉':
      return 'linear-gradient(135deg, #4299e1, #3182ce)';
    case '中吉':
      return 'linear-gradient(135deg, #9f7aea, #805ad5)';
    case '小吉':
      return 'linear-gradient(135deg, #ed8936, #dd6b20)';
    case '凶':
      return 'linear-gradient(135deg, #f56565, #e53e3e)';
    case '大凶':
      return 'linear-gradient(135deg, #742a2a, #c53030)';
    default:
      return 'linear-gradient(135deg, #718096, #4a5568)';
  }
}

// 格の日本語名マッピング
const kakuNames = {
  tenkaku: '天格',
  jinkaku: '人格',
  chikaku: '地格',
  gaikaku: '外格',
  sokaku: '総格'
};

// 格の説明
const kakuExplanations = {
  tenkaku: '先祖運・家系運を表し、晩年の運勢に影響',
  jinkaku: '主運・性格運を表し、人生の中心となる運勢',
  chikaku: '幼年運・基礎運を表し、成長期の運勢に影響',
  gaikaku: '対人運・社会運を表し、周囲との関係性に影響',
  sokaku: '総運・生涯運を表し、人生全体の運勢を示す'
};

function ResultDisplay({ result, lastName, firstName }) {
  const { characters = [], gogaku = {}, overall = "不明" } = result;

  return (
    <ResultContainer>
      <NameTitle>{lastName} {firstName} さん</NameTitle>
      
      <OverallResult result={overall}>
        総合判定: {overall}
      </OverallResult>

      {/* 文字と画数の表示 */}
      <CharacterSection>
        <CharacterTitle>文字構成と画数</CharacterTitle>
        <CharacterGrid>
          {characters && characters.length > 0 ? (
            characters.map((char, index) => (
              <CharacterCard key={index}>
                <div className="character">{char.char}</div>
                <div className="stroke">{char.stroke}画</div>
              </CharacterCard>
            ))
          ) : (
            <CharacterCard>
              <div className="character">-</div>
              <div className="stroke">-</div>
            </CharacterCard>
          )}
        </CharacterGrid>
      </CharacterSection>

      {/* 五格の詳細結果 */}
      <GogakuSection>
        <GogakuTitle>五格説による詳細診断</GogakuTitle>
        <GogakuGrid>
          {gogaku && Object.keys(gogaku).length > 0 ? (
            Object.entries(gogaku).map(([key, value]) => (
              <GogakuCard key={key}>
                <KakuName>
                  {kakuNames[key] || key}
                  <KakuValue>{value.value}画</KakuValue>
                </KakuName>
                
                <KakuResult result={value.result}>
                  {value.result}
                </KakuResult>
                
                <KakuDescription>
                  <strong>{kakuExplanations[key] || "説明なし"}</strong><br />
                  {value.description || "詳細なし"}
                </KakuDescription>
              </GogakuCard>
            ))
          ) : (
            <GogakuCard>
              <KakuDescription>
                五格の詳細データがありません。
              </KakuDescription>
            </GogakuCard>
          )}
        </GogakuGrid>
      </GogakuSection>

      {/* 補足説明 */}
      <div style={{
        background: '#f7fafc',
        border: '1px solid #e2e8f0',
        borderRadius: '12px',
        padding: '20px',
        marginTop: '30px',
        textAlign: 'left'
      }}>
        <h4 style={{ color: '#2d3748', margin: '0 0 10px 0', fontSize: '16px' }}>
          診断について
        </h4>
        <ul style={{ 
          color: '#4a5568', 
          fontSize: '14px', 
          lineHeight: '1.5',
          paddingLeft: '20px',
          margin: '0'
        }}>
          <li>康熙字典準拠の画数を使用</li>
          <li>五格説による判定（江戸時代からの伝統的手法）</li>
          <li>人格と総格を重視した総合判定</li>
          <li>一文字姓名には霊数（+1画）を適用</li>
        </ul>
      </div>
    </ResultContainer>
  );
}

export default ResultDisplay;