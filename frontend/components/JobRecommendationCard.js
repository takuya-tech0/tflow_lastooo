// JobRecommendationCard.js
import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import JobCard from './JobCard';
import useJobRecommendation from '../hooks/useJobRecommendation';
import LoadingAnimation from './LoadingAnimation';
import styles from '../styles/JobRecommendationCard.module.css';

const JobRecommendationCard = ({
    userData,
    recommendationType
}) => {
    const [topJobs, setTopJobs] = useState({});
    const [recommendations, setRecommendations] = useState({});
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const { handleJobRecommendation } = useJobRecommendation(setRecommendations, setTopJobs, setLoading, setError);

    useEffect(() => {
        handleJobRecommendation(recommendationType);
    }, [recommendationType]);

    const parseRecommendations = (rawRecommendations) => {
        if (typeof rawRecommendations === 'string' && rawRecommendations.trim() !== '') {
            const parsedRecommendations = rawRecommendations.split(/(?=\d+\.\s*推奨求人：)/).filter(Boolean);
            return parsedRecommendations.map((recommendation) => {
                const parts = recommendation.split(/\n\s*マッチング理由：\s*\n/);
                const titleAndId = parts[0].trim();
                const matchingReasons = parts[1] ? parts[1].split(/\n\s*・/).filter(Boolean).map(reason => reason.trim()) : [];
    
                const match = titleAndId.match(/\d+\.\s*推奨求人：求人ID:\s*(\d+)/);
                if (!match) {
                    console.error('Failed to parse job ID for recommendation:', titleAndId);
                    return null;
                }
                
                const [, jobId] = match;
                
                return {
                    job_post_id: parseInt(jobId),
                    matching_reasons: matchingReasons
                };
            }).filter(Boolean);
        }
        return [];
    };

    const combineJobsWithRecommendations = (jobs, recs) => {
        if (!jobs || !recs) return [];
        return jobs.map(job => {
            const recommendation = recs.find(r => r.job_post_id === job.job_id);
            return {
                ...job,
                job_post_id: job.job_id,
                matching_reasons: recommendation ? recommendation.matching_reasons : []
            };
        });
    };

    const vectorType = recommendationType === 'personality' ? 'personality_vector' : 'career_info_vector';
    const jobsToRender = topJobs[vectorType] && recommendations[vectorType]
        ? combineJobsWithRecommendations(topJobs[vectorType], parseRecommendations(recommendations[vectorType]))
        : [];

    return (
        <motion.div
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.4 }}
            className={styles.container}
        >
            <h3 className={styles.title}>AI求人提案</h3>
            <AnimatePresence>
                {loading ? (
                    <LoadingAnimation key="loading" />
                ) : (
                    <motion.div
                        key="content"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                    >
                        <div className={styles.recommendationSection}>
                            <h4>{recommendationType === 'personality' ? '性格傾向' : 'スキル'}に基づく推奨</h4>
                            <div className={styles.jobGrid}>
                                {jobsToRender.map((job, index) => (
                                    <JobCard key={`${recommendationType}-${job.job_post_id || index}`} job={job} />
                                ))}
                            </div>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>

            {error && (
                <motion.p
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className={styles.errorMessage}
                >
                    {error}
                </motion.p>
            )}

            <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => handleJobRecommendation(recommendationType)}
                disabled={loading}
                className={styles.recommendButton}
            >
                {loading ? 'AIが探しています...' : '提案してもらう'}
            </motion.button>
        </motion.div>
    );
};

export default JobRecommendationCard;