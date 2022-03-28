from ORM.Model import Instance, User, Envelope, Tree, TreeEnvelope, Commit, Head


class Committer:
    def __init__(self, session, cur_usr: User, ins: Instance):
        self.session = session
        self.cur_usr = cur_usr
        self.ins = ins

    def commit(self, message: str):
        tree = self.create_tree()
        self.create_commit(tree, message)

    def create_envelope(self, instance_field):
        envelope = Envelope(
            instance_field_id=instance_field.id,
            content_value=instance_field.value,
            updated_at=instance_field.updated_at
        )
        hash_envelope = somehashfunction(
            str(envelope.instance_field_id) +
            envelope.content_value +
            str(envelope.updated_at)
        )
        existed_envelope = self.session.query(Envelope).get(hash_envelope)
        if existed_envelope:
            return existed_envelope
        else:
            envelope.hash_envelope = hash_envelope
            self.session.add(envelope)
            self.session.flush()
            self.session.refresh(envelope)
            return envelope

    def create_tree(self):
        tree = Tree()
        for i_f in self.ins.instances_fields:
            envelope = self.create_envelope(i_f)
            tree.trees_envelopes.append(TreeEnvelope(hash_envelope=envelope.hash_envelope))
        hash_tree = somehashfunction(
            ''.join([te.hash_envelope for te in tree.trees_envelopes])
        )
        existed_tree = self.session.query(Tree).get(hash_tree)
        if existed_tree:
            return existed_tree
        else:
            tree.hash_tree = hash_tree
            self.session.add(tree)
            self.session.flush()
            self.session.refresh(tree)
            return tree

    def create_commit(self, tree, message: str):
        head = self.ins.head
        if head:
            prev_commit = head.last_commit
            import datetime
            commit = Commit(
                prev_hash_commit=prev_commit.hash_commit,
                hash_tree=tree.hash_tree,
                creator_id=self.cur_usr.id,
                instance_id=self.ins.id,
                created_at=datetime.datetime.now(),
                current_phase_id=self.ins.current_phase_id
            )
        else:
            import datetime
            commit = Commit(
                hash_tree=tree.hash_tree,
                creator_id=self.cur_usr.id,
                instance_id=self.ins.id,
                created_at=datetime.datetime.now(),
                current_phase_id=self.ins.current_phase_id
            )
            new_head = Head(instance_id=self.ins.id)
            head = new_head
        hash_commit = somehashfunction(
            commit.prev_hash_commit if commit.prev_hash_commit is not None else '' +
            commit.hash_tree +
            str(commit.creator_id) +
            str(commit.instance_id) +
            str(commit.created_at) +
            str(commit.current_phase_id)
        )
        commit.hash_commit = hash_commit
        commit.message = message
        self.session.add(commit)
        self.session.flush()
        self.session.refresh(commit)
        head.last_commit = commit
        return commit

    def checkout(self, hash_commit):
        commit = self.session.query(Commit).get(hash_commit)
        akey = "superstrongkey"
        if not commit:
            raise Exception('Commit is not existed')
        else:
            tree = commit.tree
            decrypted_contents = [sdecrypt(t_e.envelope.encrypted_content, akey) for t_e in tree.trees_envelopes]
            return decrypted_contents


def somehashfunction(txt):
    import hashlib
    encoded_text = txt.encode()
    hash_digest = hashlib.sha256(encoded_text).hexdigest()
    return hash_digest


def sencrypt(txt: str, skey):
    text = txt if txt is not None else ''
    return 'encryptedwith_' + skey + text


def sign(txt: str):
    text = txt if txt is not None else ''
    return 'signed_' + text


def sdecrypt(txt: str, skey):
    return txt.replace('encryptedwith_' + skey, '')
