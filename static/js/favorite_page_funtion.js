$(document).ready(function () {
    show_favorite_feed()
});

function show_favorite_feed() {
    $.ajax({
        type: 'GET',
        url: "",
        data: {},
        success: function (response) {
            let favorite_feeds = response['favorite_feeds']
            for (let i = 0; i < favorite_feeds.length; i++) {
                let feed_user_profile_img = favorite_feeds[i]['feed_user_profile_img']
                let feed_user_name = favorite_feeds[i]['feed_user_name']
                let feed_user_uploaded_picture = favorite_feeds[i]['feed_user_uploaded_picture']

                let get_data_cnt = 0
                let temp_html = `<div id="favorite_feed" class="favorite-feed">
                                     <div class="user-name-and-img">
                                        <div class="feed-user-img">
                                            <button class="user-page-img-btn">
                                                <img src="${feed_user_profile_img}">
                                            </button>
                                        </div>
                                        <p class="feed-user-name">${feed_user_name}</p>
                                     </div>
                                     <img src="${feed_user_uploaded_picture}">
                                 </div>`
                $('#favorite_feed').append(temp_html)
                get_data_cnt += 1

                if (get_data_cnt > 3) {
                    setTimeout($('#favorite_feed').append(temp_html),1000)
                    get_data_cnt += 1
                }
            }
        }
    })
}

function to_main() {
    location.href = "main_page.html"
}

function to_search() {
    location.href = '../templates/search_page.html'
}

function to_upload() {
    location.href = '../templates/upload_img_and_writing_page.html'
}

function to_favorite() {
    location.href = "../templates/favorite_page.html"
}

function to_my_pg() {
    location.href = "../templates/mypage.html"
}

function to_user_pg() {
    location.href = '../templates/other_user_page.html'
}
