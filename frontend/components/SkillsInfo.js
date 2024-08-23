import { motion } from 'framer-motion';
import styles from '../styles/SkillsInfo.module.css';

export default function SkillsInfo({ skills }) {
    return (
        <motion.div
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.5 }}
            className={styles.section}
        >
            <h2>スキル情報</h2>
            <div className={styles.skillsContainer}>
                {skills.map((skill, index) => (
                    <motion.span
                        key={index}
                        className={styles.skillCard}
                        initial={{ scale: 0.8, opacity: 0 }}
                        animate={{ scale: 1, opacity: 1 }}
                        transition={{ delay: 0.05 * index }}
                    >
                        {skill.skill_name}
                    </motion.span>
                ))}
            </div>
        </motion.div>
    );
}