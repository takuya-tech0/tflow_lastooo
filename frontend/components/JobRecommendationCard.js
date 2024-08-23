// JobRecommendationCard.js
import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import JobCard from './JobCard';
import useJobRecommendation from '../hooks/useJobRecommendation';
import LoadingAnimation from './LoadingAnimation';
import styles from '../styles/JobRecommendationCard.module.css';

const JobRecommendationCard = ({
    userData,
    loading,
    setLoading,
    error,
    setError
}) => {
    const [topJobs, setTopJobs] = useState([]);
    const [recommendations, setRecommendations] = useState('');
    const { handleJobRecommendation } = useJobRecommendation(setRecommendations, setTopJobs, setLoading, setError);

    useEffect(() => {
        handleJobRecommendation();
    }, []);

    useEffect(() => {
        console.log("Raw recommendations:", recommendations);
    }, [recommendations]);

    const parseRecommendations = (rawRecommendations) => {
        console.log("Parsing recommendations:", rawRecommendations);
        
        if (typeof rawRecommendations === 'string' && rawRecommendations.trim() !== '') {
            const parsedRecommendations = rawRecommendations.split(/\d+\.\s推奨求人：/).filter(Boolean);
            console.log("Split recommendations:", parsedRecommendations);
            
            return parsedRecommendations.map((recommendation, index) => {
                console.log(`Processing recommendation ${index + 1}:`, recommendation);
                
                const parts = recommendation.split(/\n\s*マッチング理由：\n/);
                console.log(`Parts for recommendation ${index + 1}:`, parts);
                
                const titleAndId = parts[0];
                const rest = parts.slice(1);
                
                console.log(`Title and ID for recommendation ${index + 1}:`, titleAndId);
                console.log(`Rest for recommendation ${index + 1}:`, rest);
                
                const match = titleAndId.match(/(.+)（求人ID:\s*(\d+)）/);
                if (!match) {
                    console.error(`Failed to parse job title and ID for recommendation ${index + 1}:`, titleAndId);
                    return null;
                }
                
                const [, jobTitle, jobId] = match;
                console.log(`Parsed job title: "${jobTitle}", job ID: ${jobId}`);
                
                let matchingReasons = [];
                if (rest.length > 0 && rest[0]) {
                    matchingReasons = rest[0].split(/\n\s*・/).filter(Boolean).map(reason => reason.trim());
                    console.log(`Matching reasons for recommendation ${index + 1}:`, matchingReasons);
                } else {
                    console.warn(`No matching reasons found for recommendation ${index + 1}`);
                }
                
                return {
                    job_post_id: parseInt(jobId),
                    job_title: jobTitle,
                    matching_reasons: matchingReasons
                };
            }).filter(Boolean);
        } else if (Array.isArray(rawRecommendations)) {
            console.log("rawRecommendations is already an array:", rawRecommendations);
            return rawRecommendations;
        }
        
        console.warn("Invalid rawRecommendations format:", rawRecommendations);
        return [];
    };

    const parsedRecommendations = parseRecommendations(recommendations);
    console.log("Parsed recommendations:", parsedRecommendations);

    const combinedJobs = topJobs.map(job => {
        const recommendation = parsedRecommendations.find(r => r.job_post_id === job.job_post_id);
        const combinedJob = {
            ...job,
            matching_reasons: recommendation ? recommendation.matching_reasons : [],
            similarity: job.similarity // similarityを追加
        };
        console.log(`Job ${job.job_post_id} matching reasons:`, combinedJob.matching_reasons);
        return combinedJob;
    });

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
                        {combinedJobs.length > 0 ? (
                            <div className={styles.jobGrid}>
                                {combinedJobs.map((job) => (
                                    <JobCard key={job.job_post_id} job={job} />
                                ))}
                            </div>
                        ) : (
                            <p className={styles.noJobs}>{userData.employee_info.name}さんに最適な求人を提案します</p>
                        )}
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
                onClick={handleJobRecommendation}
                disabled={loading}
                className={styles.recommendButton}
            >
                {loading ? 'AIが探しています...' : '提案してもらう'}
            </motion.button>
        </motion.div>
    );
};

export default JobRecommendationCard;