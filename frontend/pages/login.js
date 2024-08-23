import { useState } from 'react';
import LoginForm from '../components/LoginForm';
import LoginBrand from '../components/LoginBrand';
import styles from '../styles/Login.module.css';

export default function Login() {
    const [isSuccess, setIsSuccess] = useState(false);

    return (
        <div className={styles.loginContainer}>
            <div className={styles.loginLeft}>
                <LoginBrand />
            </div>
            <div className={styles.loginRight}>
                <LoginForm setIsSuccess={setIsSuccess} isSuccess={isSuccess} />
            </div>
        </div>
    );
}