// useJobRecommendation.js
import axios from 'axios';

export default function useJobRecommendation(setRecommendations, setTopJobs, setLoading, setError) {
    const handleJobRecommendation = async () => {
        console.log("handleJobRecommendation called");
        setLoading(true);
        setError('');
        try {
            const token = localStorage.getItem('token');
            console.log("Token retrieved:", token ? "Token exists" : "No token");
            const response = await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/recommendations`, null, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            });

            console.log("API Response:", response.data);

            const { recommendations, top_jobs } = response.data;

            // Log to verify the data structure of top_jobs
            console.log("Raw recommendations:", recommendations);
            console.log("Raw top_jobs:", top_jobs);  // Check if this logs correctly
            
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
