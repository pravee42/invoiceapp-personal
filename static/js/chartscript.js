async function GetData() {
    const res = axios.get('/api/chart/');
    console.log(res.data);
}