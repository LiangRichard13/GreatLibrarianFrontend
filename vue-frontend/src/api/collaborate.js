import service from "@/utils/request";

export function getUserList() {
    return service({
        url: '/collaborate/getUserList',
        method: 'get',
    })
}
export function addFriend(data) {
    return service({
        url: '/collaborate/addFriend',
        method: 'post',
        data:data
    })
}

export function getUserFriendsById(id) {
    return service({
        url: '/collaborate/addFriend/'+id,
        method: 'get',
    })
}

export function deleteFriendById(id) {
    return service({
        url: '/collaborate/addFriend/'+id,
        method: 'get',
    })
}