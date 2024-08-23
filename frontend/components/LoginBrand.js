import { motion } from 'framer-motion';
import styles from '../styles/Login.module.css';

export default function LoginBrand() {
    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className={styles.loginBrand}
        >
            <img src="/images/TF_logo.png" alt="Talent Flow Logo" className={styles.logo} />
            <h1>AIによる最適な人事配置を実現</h1>
            <h2>Talent Flow</h2>
        </motion.div>
    );
}