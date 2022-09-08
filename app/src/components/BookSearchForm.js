import React, { useState, useEffect } from 'react';
/**
 * book search form 
 * @param {*} param0 the setBookSearch function
 */
function BookSearchForm({setBookSearch}) {
    const [bookField, setBookField] = useState(""); 
    const [bookQuery, setBookQuery] = useState(""); 
    return (
        <div class="col-md-3">
        <form className="border p-3">
            <div className="form-group">
                <label for="bookSearchOptions">Search Books</label>
                <select id="bookSearchOptions" className="form-control" onChange={e => setBookField(e.target.value)}>
                    <option selected value="book_id">ID</option>
                    <option value="title">Title</option>
                    <option value="isbn">ISBN</option>
                    <option value="author">Author</option>
                    <option value="rating">Rating</option>
                    <option value="rating_count">Rating Count</option>
                    <option value="review_count">Review Count</option>
                </select>
            </div>
            <div className="form-group">
                <label for="bookSearchQuery">Query</label>
                <input type="text" className="form-control" id="bookSearchQuery" onChange={e => setBookQuery(e.target.value)}></input>
            </div>
            <div className="form-group">
                <button type="button" className="btn btn-outline-secondary btn-block" id="bookSearch" onClick={() => setBookSearch(bookField, bookQuery)}>Search</button>
            </div>
        </form>
        </div>
    );
}

export default BookSearchForm;