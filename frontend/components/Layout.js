import Head from 'next/head';
import Link from 'next/link';
import useAuth from '../hooks/useAuth';
import styles from '../styles/Layout.module.css';

export default function Layout({ children }) {
  const { logout } = useAuth();

  return (
    <div className={styles.container}>
      <Head>
        <title>TalentFlow</title>
        <meta name="description" content="AIによる最適な人事配置を実現" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <header className={styles.header}>
        <div className={styles.logoContainer}>
          <img src="/images/TF_logo.png" alt="TalentFlow Logo" className={styles.logo} />
          <h1>TalentFlow</h1>
        </div>
        <nav>
          <ul>
            <li><Link href="/">Home</Link></li>
            <li><Link href="/job_recommendation">Job Recommendations</Link></li>
            <li><Link href="/mypage">My Page</Link></li>
            <li><button onClick={logout}>Logout</button></li>
          </ul>
        </nav>
      </header>

      <main>{children}</main>

      <footer className={styles.footer}>
        <p>&copy; 2024 TalentFlow. All rights reserved.</p>
      </footer>
    </div>
  );
}