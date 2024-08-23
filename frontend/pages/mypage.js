import { useState } from 'react';
import { useRouter } from 'next/router';
import { motion, AnimatePresence } from 'framer-motion';
import Layout from '../components/Layout';
import UserProfile from '../components/UserProfile';
import PsychographicChart from '../components/PsychographicChart';
import CareerInfo from '../components/CareerInfo';
import SkillsInfo from '../components/SkillsInfo';
import LoadingSpinner from '../components/LoadingSpinner';
import useUserData from '../hooks/useUserData';
import styles from '../styles/MyPage.module.css';

export default function MyPage() {
  const router = useRouter();
  const { userData, loading, error } = useUserData();

  return (
    <Layout>
      <div className={styles.mypageContainer}>
        <AnimatePresence>
          {loading ? (
            <LoadingSpinner key="loading" />
          ) : error ? (
            <motion.p
              key="error"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className={styles.error}
            >
              {error}
            </motion.p>
          ) : userData && (
            <motion.div
              key="content"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className={styles.contentWrapper}
            >
              <UserProfile userData={userData} />
              <main className={styles.mainContent}>
                <div className={styles.sectionContainer}>
                  <PsychographicChart spiData={userData.spi} />
                  <CareerInfo evaluations={userData.evaluations} />
                </div>
                <SkillsInfo skills={userData.skills} />
                <div className={styles.buttons}>
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={() => alert('評価・コメント閲覧')}
                  >
                    評価・コメント閲覧
                  </motion.button>
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={() => router.push('/job_recommendation')}
                  >
                    求人推薦システム
                  </motion.button>
                </div>
              </main>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </Layout>
  );
}