import service from "@/utils/request";

export function getUserList(id) {
    return service({
        url: '/user/getUserList',
        method: 'get',
        params: {
            id: id
        }
    })
}

export function addFriend(data) {
    return service({
        url: '/friend',
        method: 'post',
        data: data
    })
}

export function getUserFriendsById(id) {
    return service({
        url: '/user/getUserList',
        method: 'get',
        params: {
            id: id
        }
    })
}

export function getFriendsRequest(id) {
    return service({
        url: '/collaborate/getFriendsRequest',
        method: 'get',
        params: {
            id: id
        }
    })
}

export function deleteById(id, uid) {
    return service({
        url: '/collaborate/deleteById',
        method: 'delete',
        params: {
            id: id,
            uid: uid
        }
    })
}

export function handleFriendRequest(data) {
    return service({
        url: '/friend',
        method: 'put',
        data: data
    })
}

// export function refuseToAdd(id) {
//     return service({
//         url: '/collaborate/getFriendsRequest',
//         method: 'put',
//         params: {
//             id: id
//         }
//     })
// }