//job_recommendation.js
import { useState } from 'react';
import Layout from '../components/Layout';
import UserProfile from '../components/UserProfile';
import JobRecommendationCard from '../components/JobRecommendationCard';
import useUserData from '../hooks/useUserData';
import styles from '../styles/JobRecommendation.module.css';

export default function JobRecommendation() {
    const { userData, error: userDataError } = useUserData();
    const [recommendations, setRecommendations] = useState([]);
    const [topJobs, setTopJobs] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    if (userDataError) {
        return <div className={styles.error}>Error: {userDataError}</div>;
    }

    if (!userData) {
        return <div className={styles.loading}>Loading...</div>;
    }

    return (
        <Layout>
            <div className={styles.jobRecommendationContainer}>
                <div className={styles.content}>
                    <UserProfile userData={userData} />
                    <main className={styles.mainContent}>
                        <JobRecommendationCard
                            userData={userData}
                            recommendations={recommendations}
                            setRecommendations={setRecommendations}
                            topJobs={topJobs}
                            setTopJobs={setTopJobs}
                            loading={loading}
                            setLoading={setLoading}
                            error={error}
                            setError={setError}
                        />
                    </main>
                </div>
            </div>
        </Layout>
    );
}