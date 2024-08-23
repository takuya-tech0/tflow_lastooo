import { motion } from 'framer-motion';
import styles from '../styles/LoadingSpinner.module.css';

export default function LoadingSpinner() {
    return (
        <motion.div
            key="loading"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className={styles.loading}
        >
            Loading...
        </motion.div>
    );
}