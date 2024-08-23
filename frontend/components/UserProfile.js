import { motion } from 'framer-motion';
import styles from '../styles/UserProfile.module.css';

export default function UserProfile({ userData }) {
    return (
        <motion.aside
            initial={{ x: -50, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            transition={{ delay: 0.3 }}
            className={styles.sidebar}
        >
            <img src="/images/profile.png" alt="Profile" className={styles.profileImage} />
            <ul className={styles.profileInfo}>
                <li><strong>氏名:</strong> {userData.employee_info.name}</li>
                <li><strong>社員番号:</strong> {userData.employee_info.id}</li>
                <li><strong>部署:</strong> {userData.departments[0].department_name}</li>
            </ul>
        </motion.aside>
    );
}