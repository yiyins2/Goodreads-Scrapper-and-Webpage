import React, { useState, useEffect } from 'react';
/**
 * author search form 
 * @param {*} param0 the setAuthorSearch function 
 */
function AuthorSearchForm({setAuthorSearch}) {
    const [authorField, setAuthorField] = useState(""); 
    const [authorQuery, setAuthorQuery] = useState(""); 
    return (
        <div className="col-md-3 mb-3 p-0">
        <form className="border p-3">
            <div className="form-group">
            <label for="authorSearchOptions">Search Authors</label>
            <select id="authorSearchOptions" className="form-control" onChange={e => setAuthorField(e.target.value)}>
                <option selected value="author_id">ID</option>
                <option value="name">Name</option>
                <option value="rating">Rating</option>
                <option value="rating_count">Rating Count</option>
                <option value="review_count">Review Count</option>
            </select>
            </div>
            <div className="form-group">
                <label for="authorSearchQuery">Query</label>
                <input type="text" className="form-control" id="authorSearchQuery" onChange={e => setAuthorQuery(e.target.value)}></input>
            </div>
            <div className="form-group">
                <button type="button" className="btn btn-outline-secondary btn-block" id="authorSearch" onClick={() => setAuthorSearch(authorField, authorQuery)}>Search</button>
            </div>
        </form>
        </div>
    );
}

export default AuthorSearchForm;