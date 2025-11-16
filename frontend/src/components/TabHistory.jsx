import { useEffect, useState } from "react";
import axios from "axios";
import QuizModal from "./QuizModal";

function TabHistory() {
  const [list, setList] = useState([]);
  const [modalData, setModalData] = useState(null);

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    const res = await axios.get("http://localhost:8000/api/quizzes");
    setList(res.data);
  };

  const openDetails = async (id) => {
    const res = await axios.get(`http://localhost:8000/api/quizzes/${id}`);
    setModalData(res.data);
  };

  return (
    <div>
      <table className="history-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>URL</th>
            <th>Date</th>
            <th>Details</th>
          </tr>
        </thead>

        <tbody>
          {list.map((item) => (
            <tr key={item.id}>
              <td>{item.id}</td>
              <td>{item.url}</td>
              <td>{item.created_at}</td>
              <td>
                <button onClick={() => openDetails(item.id)}>View</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {modalData && (
        <QuizModal data={modalData} onClose={() => setModalData(null)} />
      )}
    </div>
  );
}

export default TabHistory;
