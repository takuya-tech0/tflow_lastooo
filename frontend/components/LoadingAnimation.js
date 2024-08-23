import { motion } from 'framer-motion';
import styles from '../styles/LoadingAnimation.module.css';

export default function LoadingAnimation() {
    return (
        <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className={styles.loadingContainer}
        >
            <div className={styles.loadingSpinner}>
                <div className={`${styles.circle} ${styles.circle1}`}></div>
                <div className={`${styles.circle} ${styles.circle2}`}></div>
                <div className={`${styles.circle} ${styles.circle3}`}></div>
            </div>
            <motion.p
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.5 }}
            >
                最適な求人を探しています...
            </motion.p>
        </motion.div>
    );
}