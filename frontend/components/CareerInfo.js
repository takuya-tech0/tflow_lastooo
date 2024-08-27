import React from 'react';
import styles from '../styles/MyPage.module.css';

const CareerInfo = ({ personality_detail }) => {
  const paragraphs = personality_detail.split('###').filter(p => p.trim());

  const renderParagraph = (paragraph) => {
    return paragraph.split(/(?=\s*-\s*)/).map((part, index) => {
      if (part.trim().startsWith('-')) {
        return <li key={index}>{renderStrongText(part.trim().substring(1))}</li>;
      }
      return <p key={index}>{renderStrongText(part)}</p>;
    });
  };

  const renderStrongText = (text) => {
    return text.split('**').map((part, i) => 
      i % 2 === 0 ? part : <strong key={i}>{part}</strong>
    );
  };

  return (
    <div className={styles.careerInfo}>
      {paragraphs.map((paragraph, index) => (
        <div key={index} className={styles.paragraph}>
          {renderParagraph(paragraph)}
        </div>
      ))}
    </div>
  );
};

export default CareerInfo;