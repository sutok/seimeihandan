import React, { useEffect } from 'react';
import styled from 'styled-components';
import AffiliateBanner from './AffiliateBanner';

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
  // useEffect(() => {
  //   // もしもアフィリエイトのスクリプトを動的に読み込み
  //   const script = document.createElement('script');
//     script.type = 'text/javascript';
//     script.innerHTML = `
// (function(b,c,f,g,a,d,e){b.MoshimoAffiliateObject=a;
// b[a]=b[a]||function(){arguments.currentScript=c.currentScript
// ||c.scripts[c.scripts.length-2];(b[a].q=b[a].q||[]).push(arguments)};
// c.getElementById(a)||(d=c.createElement(f),d.src=g,
// d.id=a,e=c.getElementsByTagName("body")[0],e.appendChild(d))})
// (window,document,"script","//dn.msmstatic.com/site/cardlink/bundle.js?20220329","msmaflink");
// msmaflink({"n":"【公式販売】CONC リンクル インジェクション 2.5mL ｜ コンク マイクロニードル 美容液 目元 口元 シワ リンクル美容液 エイジングケア ハリ 弾力 部分美容液 レチノール 痛いコスメ 美容医療コスメ 針美容液","b":"","t":"","d":"https:\/\/thumbnail.image.rakuten.co.jp","c_p":"\/@0_mall\/midorimushishop\/cabinet","p":["\/thumb\/normal\/ml17490100_250725.jpg","\/flick\/2024\/ml17490100_0222_01.jpg","\/flick\/2025\/ml17490100_0324_02.jpg"],"u":{"u":"https:\/\/item.rakuten.co.jp\/midorimushishop\/ml17490100\/","t":"rakuten","r_v":""},"v":"2.1","b_l":[{"id":2,"u_tx":"楽天市場で見る","u_bc":"#f76956","u_url":"https:\/\/item.rakuten.co.jp\/midorimushishop\/ml17490100\/","a_id":5169165,"p_id":54,"pl_id":27059,"pc_id":54,"s_n":"rakuten","u_so":1}],"eid":"Fnih6","s":"s"});
//     `;
//     document.head.appendChild(script);
    
//     return () => {
//       // クリーンアップ
//       document.head.removeChild(script);
//     };
//   }, []);

  return (
    <HeaderContainer>
      <Logo>姓名判断アプリ</Logo>
        {/* <div id="msmaflink-Fnih6">アフィリエイトリンクを読み込み中...</div> */}
      <AffiliateBanner 
        title=""
        description="リンクルインジェクション 2.5mL マイクロニードル ニードルセラム 針美容液 ほうれい線 ハリ 弾力 目の下 目元 口元 ニードルショット ニードル美容液 レチノール配合"
        buttonText="Amazonで見る"
        buttonUrl="https://www.amazon.co.jp/CONC-%E3%83%AA%E3%83%B3%E3%82%AF%E3%83%AB%E3%82%A4%E3%83%B3%E3%82%B8%E3%82%A7%E3%82%AF%E3%82%B7%E3%83%A7%E3%83%B3-2-5ml-%E3%83%8B%E3%83%BC%E3%83%89%E3%83%AB%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88-%E3%83%AC%E3%83%81%E3%83%8E%E3%83%BC%E3%83%AB/dp/B0C855Y9MD/ref=sr_1_1_sspa?crid=1W84A1IJLXZYS&dib=eyJ2IjoiMSJ9.HflnnI6sGlYShM6teojnTp-lWDmcL3eG1G9TmcjcRxKvP2CHoRfWhbqDhL98W4ZEhvIAIKa0M8J3Xj7hXkBjoRM90F3urIYSEUBYcn7tYLYxRlLgJxbukCAcCn4TuUOz-VhduB_miGXOiVdDCn_dQs6ne046msAq9YAt2qftNl0qEsIaY8tUfH8PxU8YCAQ4rYjm1ggXXVk_esAf9B0TYwGNXm5_g04K74ye2gnjuqHIqVVg4Ea4yUuEQEAMnCI1fcvc_-sv3FRx5DHAN9CLHajmODJBHOttMcohnPkmilY.AU4jL7YA_YvZuRb8Ey6XCiwqf-gilTt9JRBfiUTogcY&dib_tag=se&keywords=%E3%83%A6%E3%83%BC%E3%82%B0%E3%83%AC%E3%83%8A+%E3%83%AA%E3%83%B3%E3%82%AF%E3%83%AB%E3%82%A4%E3%83%B3%E3%82%B8%E3%82%A7%E3%82%AF%E3%82%B7%E3%83%A7%E3%83%B3&qid=1757723788&sprefix=%E3%83%A6%E3%83%BC%E3%82%B0%E3%83%AC%E3%83%8A%E3%80%80%E3%83%AA%E3%83%B3%E3%82%AF%E3%83%AB%2Caps%2C183&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1"
      />
    </HeaderContainer>
  );
}

export default Header;