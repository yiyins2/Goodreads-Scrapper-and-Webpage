import React, { useState, useEffect } from 'react';
/**
 * book add form 
 * @param {*} param0 the authorAdd function 
 */
function AuthorAddForm({authorAdd}) {
    const [author, setAuthor] = useState({}); 
    return (
        <div class="col-md-8 mb-3">
        <form className="border p-3">
        <div class="form-row">
            <div className="form-group col-md-3">
                <label for="authorID">Author ID</label>
                <input type="text" className="form-control" id="authorID" onChange={e => setAuthor({...author, author_id: e.target.value})}></input>
            </div>
            <div className="form-group col-md-3">
                <label for="authorName">Name</label>
                <input type="text" className="form-control" id="authorName" onChange={e => setAuthor({...author, name: e.target.value})}></input>
            </div>
            <div className="form-group col-md-3">
                <label for="authorURL">Author URL</label>
                <input type="text" className="form-control" id="authorURL" onChange={e => setAuthor({...author, author_url: e.target.value})}></input>
            </div>
            <div className="form-group col-md-3">
                <label for="authorImg">Image URL</label>
                <input type="text" className="form-control" id="authorImg" onChange={e => setAuthor({...author, image_url: e.target.value})}></input>
            </div>
        </div>
        <div class="form-row">
            <div className="form-group col-md-4">
                <label for="authorRating">Rating</label>
                <input type="text" className="form-control" id="authorRating" onChange={e => setAuthor({...author, rating: e.target.value})}></input>
            </div>
            <div className="form-group col-md-4">
                <label for="authorRatingCount">Rating Count</label>
                <input type="text" className="form-control" id="authorRatingCount" onChange={e => setAuthor({...author, rating_count: e.target.value})}></input>
            </div>
            <div className="form-group col-md-4">
                <label for="authorReviewCount">Review Count</label>
                <input type="text" className="form-control" id="authorReviewCount" onChange={e => setAuthor({...author, review_count: e.target.value})}></input>
            </div>
        </div>
        <div className="form-group">
            <button type="button" className="btn btn-outline-secondary btn-block" id="authorAdd" onClick={() => authorAdd(author)}>Add Author</button>
        </div>
        </form>
        </div>
    );
}

export default AuthorAddForm;