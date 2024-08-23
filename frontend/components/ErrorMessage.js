import { motion } from 'framer-motion';
import styles from '../styles/Login.module.css';

export default function ErrorMessage({ message }) {
    return (
        <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className={styles.errorMessage}
        >
            {message}
        </motion.div>
    );
}