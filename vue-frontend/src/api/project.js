import service from "@/utils/request";

export function addProject(data) {
    return service({
        url: '/project/addProject',
        method: 'post',
        data: data
    })
}
export function getProjectsById(id) {
    return service({
        url: '/project/addProject/'+id,
        method: 'get',
    })
}