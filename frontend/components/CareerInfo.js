import { motion } from 'framer-motion';
import styles from '../styles/CareerInfo.module.css';

export default function CareerInfo({ evaluations }) {
    return (
        <motion.div
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.4 }}
            className={styles.section}
        >
            <h2>評価履歴</h2>
            <ul className={styles.evaluationList}>
                {evaluations.map((evaluation, index) => (
                    <motion.li
                        key={index}
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.1 * index }}
                    >
                        <span className={styles.year}>{evaluation.year}:</span>
                        <span className={styles.evaluation}>{evaluation.evaluation}</span>
                        <div className={styles.comment}>
                            <strong>コメント:</strong> {evaluation.comment}
                        </div>
                    </motion.li>
                ))}
            </ul>
        </motion.div>
    );
}