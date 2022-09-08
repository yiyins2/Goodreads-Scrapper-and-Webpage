import React, { useState, useEffect } from 'react';
/**
 * book add form 
 * @param {*} param0 the bookAdd function 
 */
function BookAddForm({bookAdd}) {
    const [book, setBook] = useState({}); 

    return (
        <div class="col-md-8 mb-3">
        <form className="border p-3">
        <div class="form-row">
            <div className="form-group col-md-4">
                <label for="bookID">Book ID</label>
                <input type="text" className="form-control" id="bookID" onChange={e => setBook({...book, book_id: e.target.value})}></input>
            </div>
            <div className="form-group col-md-4">
                <label for="bookTitle">Title</label>
                <input type="text" className="form-control" id="bookTitle" onChange={e => setBook({...book, title: e.target.value})}></input>
            </div>
            <div className="form-group col-md-4">
                <label for="bookURL">Book URL</label>
                <input type="text" className="form-control" id="bookURL" onChange={e => setBook({...book, book_url: e.target.value})}></input>
            </div>
        </div>
        <div class="form-row">
            <div className="form-group col-md-6">
                <label for="bookISBN">ISBN</label>
                <input type="text" className="form-control" id="bookISBN" onChange={e => setBook({...book, ISBN: e.target.value})}></input>
            </div>
            <div className="form-group col-md-6">
                <label for="bookImg">Image URL</label>
                <input type="text" className="form-control" id="bookImg" onChange={e => setBook({...book, image_url: e.target.value})}></input>
            </div>
        </div>
        <div class="form-row">
            <div className="form-group col-md-6">
                <label for="bookAuthor">Author</label>
                <input type="text" className="form-control" id="bookAuthor" onChange={e => setBook({...book, author: e.target.value})}></input>
            </div>
            <div className="form-group col-md-6">
                <label for="bookAuthorURL">Author URL</label>
                <input type="text" className="form-control" id="bookAuthorURL" onChange={e => setBook({...book, author_url: e.target.value})}></input>
            </div>
        </div>
        <div class="form-row">
            <div className="form-group col-md-4">
                <label for="bookRating">Rating</label>
                <input type="text" className="form-control" id="bookRating" onChange={e => setBook({...book, rating: e.target.value})}></input>
            </div>
            <div className="form-group col-md-4">
                <label for="bookRatingCount">Rating Count</label>
                <input type="text" className="form-control" id="bookRatingCount" onChange={e => setBook({...book, rating_count: e.target.value})}></input>
            </div>
            <div className="form-group col-md-4">
                <label for="bookReviewCount">Review Count</label>
                <input type="text" className="form-control" id="bookReviewCount" onChange={e => setBook({...book, review_count: e.target.value})}></input>
            </div>
        </div>
        <div className="form-group">
            <button type="button" className="btn btn-outline-secondary btn-block" id="bookAdd" onClick={() => bookAdd(book)}>Add Book</button>
        </div>
        </form>
        </div>
    );
}

export default BookAddForm;