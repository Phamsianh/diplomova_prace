import { Link } from "react-router-dom"
import { formatDate } from "../../utils/datetime"
import { CommitIcon } from "../icon"

export const ReadCommits = ({ commits_data }) => {
    return (
        <div className='read-commits'>
			<table>
                <thead>
                    <tr>
                        <th className="created-at">Created at</th>
                        <th className="phase-id">Phase ID</th>
                        <th className="prev-hash">Previous Commit</th>
                        <th className="hash-commit">Hash Commit</th>
                        <th className="view-commit">View commit</th>
                    </tr>
                </thead>
                <tbody>
                    {commits_data.map(cd => {
                        return (
                            <tr key={cd.hash_commit}>
                                <td className="created-at">{formatDate(cd.created_at)}</td>
                                <td className="phase-id">{cd.current_phase_id}</td>
                                <td className="prev-hash">{cd.prev_hash_commit?cd.prev_hash_commit.slice(0,16): 'first commit'}</td>
                                <td className="hash-commit">{cd.hash_commit.slice(0,16)}</td>
                                <td className="view-commit"><Link to={cd.hash_commit}><CommitIcon/></Link></td>
                            </tr>
                        )
                    })}
                </tbody>
            </table>
		</div>
    )
}
