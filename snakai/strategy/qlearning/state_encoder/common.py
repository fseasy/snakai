# coding: utf-8

def build_all_states(unit_encoders):
    _all_states = []
    def _recursive_build(encoder_idx, current_state):
        if encoder_idx == len(unit_encoders):
            full_state = tuple(current_state)
            _all_states.append(full_state)
        else:
            unit_encoder = unit_encoders[encoder_idx]
            for state_id in unit_encoder.ids:
                current_state.append(state_id)
                _recursive_build(encoder_idx + 1, current_state)
                current_state.pop()
    
    _recursive_build(0, [])
    return _all_states
