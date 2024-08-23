import { motion } from 'framer-motion';
import styles from '../styles/PsychographicChart.module.css';

export default function PsychographicChart({ spiData }) {
    const radarData = spiData ? [
        spiData.extraversion,
        spiData.agreebleness,
        spiData.conscientiousness,
        spiData.neuroticism,
        spiData.openness,
    ] : [];

    return (
        <motion.div
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.4 }}
            className={styles.section}
        >
            <h2>性格特性</h2>
            <RadarChart data={radarData} labels={['外向性', '協調性', '誠実性', '繊細性', '開放性']} />
        </motion.div>
    );
}

function RadarChart({ data, labels }) {
    const chartSize = 300;
    const centerX = chartSize / 2;
    const centerY = chartSize / 2;
    const maxValue = Math.max(...data, 70);  // 最大値を100とする
    const angleStep = (Math.PI * 2) / labels.length;

    // データポイントの座標を計算
    const points = data.map((value, index) => {
        const angle = index * angleStep - Math.PI / 2;  // -90度から開始
        const x = centerX + (value / maxValue) * (chartSize / 2 - 20) * Math.cos(angle);
        const y = centerY + (value / maxValue) * (chartSize / 2 - 20) * Math.sin(angle);
        return `${x},${y}`;
    }).join(' ');

    return (
        <svg className={styles.radarChart} viewBox={`0 0 ${chartSize} ${chartSize}`}>
            {/* 背景の円と軸 */}
            {[0.2, 0.4, 0.6, 0.8, 1].map((scale, i) => (
                <circle
                    key={i}
                    cx={centerX}
                    cy={centerY}
                    r={(chartSize / 2 - 20) * scale}
                    fill="none"
                    stroke="#ccc"
                    strokeWidth="0.5"
                />
            ))}
            {labels.map((_, index) => {
                const angle = index * angleStep - Math.PI / 2;
                const x2 = centerX + (chartSize / 2 - 20) * Math.cos(angle);
                const y2 = centerY + (chartSize / 2 - 20) * Math.sin(angle);
                return (
                    <line
                        key={index}
                        x1={centerX}
                        y1={centerY}
                        x2={x2}
                        y2={y2}
                        stroke="#ccc"
                        strokeWidth="0.5"
                    />
                );
            })}

            {/* データポリゴン */}
            <polygon
                points={points}
                fill="rgba(255, 165, 0, 0.5)"
                stroke="#FFA500"
                strokeWidth="2"
            />

            {/* ラベル */}
            {labels.map((label, index) => {
                const angle = index * angleStep - Math.PI / 2;
                const x = centerX + (chartSize / 2 - 10) * Math.cos(angle);
                const y = centerY + (chartSize / 2 - 10) * Math.sin(angle);
                return (
                    <text
                        key={index}
                        x={x}
                        y={y}
                        textAnchor="middle"
                        dominantBaseline="middle"
                        fontSize="12"
                        fill="#333"
                    >
                        {label}
                    </text>
                );
            })}
        </svg>
    );
}