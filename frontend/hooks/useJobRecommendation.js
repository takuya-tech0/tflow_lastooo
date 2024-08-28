// useJobRecommendation.js
import axios from 'axios';

export default function useJobRecommendation(setRecommendations, setTopJobs, setLoading, setError) {
    const handleJobRecommendation = async (vectorType) => {
        console.log("handleJobRecommendation called with vectorType:", vectorType);
        setLoading(true);
        setError('');
        try {
            const token = localStorage.getItem('token');
            console.log("Token retrieved:", token ? "Token exists" : "No token");
            const response = await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/recommendations`, { vector_type: vectorType }, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            });

            console.log("API Response:", response.data);

            const { recommendations, top_jobs } = response.data;

            console.log("Raw recommendations:", recommendations);
            console.log("Raw top_jobs:", top_jobs);
            
            setRecommendations(recommendations || {});
            setTopJobs(top_jobs || {});
            
        } catch (error) {
            console.error('Failed to fetch job recommendations:', error);
            setError('求人推薦の取得に失敗しました。');
        }
        setLoading(false);
    };

    return { handleJobRecommendation };
}