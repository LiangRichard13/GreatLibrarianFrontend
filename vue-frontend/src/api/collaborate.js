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

export function getFriendsRequest(id) {
    return service({
        url: '/friend',
        method: 'get',
        params: {
            uid: id
        }
    })
}

export function deleteById(id, uid) {
    return service({
        url: '/friend',
        method: 'delete',
        params: {
            fid: id,
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

export function addFriendsToExperiment(data) {
    return service({
        url: '/testProjectUser',
        method: 'post',
        data: data
    })
}

export function getFriendsByExperimentId(TPid) {
    return service({
        url: '/testProjectUser',
        method: 'get',
        params: {
            TPid: TPid,
            choose: 1
        }
    })
}

export function getExperimentsByUserId(uid) {
    return service({
        url: '/testProjectUser',
        method: 'get',
        params: {
            uid: uid,
            choose:2
        }
    })
}