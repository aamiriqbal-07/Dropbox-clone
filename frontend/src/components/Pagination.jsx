// src/components/Pagination.jsx
export default function Pagination({ total, limit, offset, onPageChange }) {
    const currentPage = Math.floor(offset / limit) + 1;
    const totalPages = Math.ceil(total / limit);
  
    const handlePrev = () => {
      if (offset - limit >= 0) {
        onPageChange(offset - limit);
      }
    };
  
    const handleNext = () => {
      if (offset + limit < total) {
        onPageChange(offset + limit);
      }
    };
  
    return (
      <div className="pagination">
        <button onClick={handlePrev} disabled={offset === 0}>
          Previous
        </button>
        <span>
          Page {currentPage} of {totalPages}
        </span>
        <button onClick={handleNext} disabled={offset + limit >= total}>
          Next
        </button>
      </div>
    );
  }