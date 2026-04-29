((ip.dst_ctx1 = ip.src_ctx0) AND (ip.src_ctx1 = ip.dst_ctx0) AND (tcp.len_ctx0 > 0) AND (tcp.len_ctx1 > 0)) -> (tcp.options.timestamp.tsecr_ctx1 <= tcp.options.timestamp.tsval_ctx0)
((ip.dst_ctx0 = ip.dst_ctx1) AND (ip.src_ctx0 = ip.src_ctx1) AND (NOT ((tcp.flags_ctx0 = 1) OR (tcp.flags_ctx0 = 2) OR (tcp.flags_ctx0 = 17) OR (tcp.flags_ctx0 = 18))) AND (NOT ((tcp.flags_ctx1 = 1) OR (tcp.flags_ctx1 = 2) OR (tcp.flags_ctx1 = 17) OR (tcp.flags_ctx1 = 18)))) -> (tcp.seq_ctx1 >= (tcp.len_ctx0 + tcp.seq_ctx0))
ip.len_ctx0 = ((ip.hdr_len_ctx0 + tcp.hdr_len_ctx0) + tcp.len_ctx0)
(ip.ttl_ctx0 <= 255) AND (ip.ttl_ctx0 > 0)
MOD(tcp.hdr_len_ctx2, 4) = 0
((ip.src_ctx1 = ip.dst_ctx2) AND (ip.src_ctx2 = ip.dst_ctx1) AND (tcp.options.timestamp.tsecr_ctx2 = tcp.options.timestamp.tsval_ctx1) AND (tcp.len_ctx1 > 0) AND (tcp.len_ctx2 > 0)) -> (tcp.ack_ctx2 = (tcp.len_ctx1 + tcp.seq_ctx1))
((tcp.ack_ctx0 = tcp.ack_ctx1) AND (tcp.ack_ctx1 = tcp.ack_ctx2) AND (tcp.flags_ctx0 = 16) AND (tcp.flags_ctx1 = 16) AND (tcp.flags_ctx2 = 16)) -> ((ip.dst_ctx0 = ip.dst_ctx1) AND (ip.dst_ctx1 = ip.dst_ctx2) AND (ip.src_ctx0 = ip.src_ctx1) AND (ip.src_ctx1 = ip.src_ctx2))
MOD(tcp.hdr_len_ctx1, 4) = 0
((ip.src_ctx1 = ip.dst_ctx2) AND (ip.src_ctx2 = ip.dst_ctx1) AND (tcp.options.timestamp.tsecr_ctx2 = tcp.options.timestamp.tsval_ctx1) AND (tcp.len_ctx1 > 0) AND (tcp.len_ctx2 > 0)) -> (tcp.ack_ctx2 = (tcp.len_ctx1 + tcp.seq_ctx1))
(ip.ttl_ctx2 <= 255) AND (ip.ttl_ctx2 > 0)
((ip.dst_ctx1 = ip.dst_ctx2) AND (ip.src_ctx1 = ip.src_ctx2) AND (NOT ((tcp.flags_ctx1 = 1) OR (tcp.flags_ctx1 = 2) OR (tcp.flags_ctx1 = 17) OR (tcp.flags_ctx1 = 18))) AND (NOT ((tcp.flags_ctx2 = 1) OR (tcp.flags_ctx2 = 2) OR (tcp.flags_ctx2 = 17) OR (tcp.flags_ctx2 = 18)))) -> (tcp.seq_ctx2 >= (tcp.len_ctx1 + tcp.seq_ctx1))
((ip.dst_ctx1 = ip.dst_ctx2) AND (ip.src_ctx1 = ip.src_ctx2) AND (tcp.flags_ctx1 = tcp.flags_ctx2) AND (tcp.len_ctx1 = tcp.len_ctx2) AND (tcp.seq_ctx1 = tcp.seq_ctx2)) -> (ip.dst_ctx1 = ip.dst_ctx2)
((ip.src_ctx0 = ip.dst_ctx1) AND (ip.src_ctx1 = ip.dst_ctx0) AND (tcp.options.timestamp.tsecr_ctx1 = tcp.options.timestamp.tsval_ctx0) AND (tcp.len_ctx0 > 0) AND (tcp.len_ctx1 > 0)) -> (tcp.ack_ctx1 = (tcp.len_ctx0 + tcp.seq_ctx0))
MOD(ip.hdr_len_ctx1, 4) = 0
MOD(tcp.hdr_len_ctx0, 4) = 0
((ip.src_ctx1 = ip.dst_ctx2) AND (ip.src_ctx2 = ip.dst_ctx1) AND (tcp.len_ctx1 = 0) AND (tcp.options.timestamp.tsecr_ctx2 = tcp.options.timestamp.tsval_ctx1) AND ((tcp.flags_ctx1 = 1) OR (tcp.flags_ctx1 = 2) OR (tcp.flags_ctx1 = 17) OR (tcp.flags_ctx1 = 18))) -> (tcp.ack_ctx2 = (tcp.seq_ctx1 + 1))
(ip.ttl_ctx1 <= 255) AND (ip.ttl_ctx1 > 0)
((ip.src_ctx0 = ip.dst_ctx1) AND (ip.src_ctx1 = ip.dst_ctx0) AND (tcp.len_ctx0 = 0) AND (tcp.options.timestamp.tsecr_ctx1 = tcp.options.timestamp.tsval_ctx0) AND (NOT ((tcp.flags_ctx0 = 1) OR (tcp.flags_ctx0 = 2) OR (tcp.flags_ctx0 = 17) OR (tcp.flags_ctx0 = 18)))) -> (tcp.ack_ctx1 = tcp.seq_ctx0)
((ip.src_ctx0 = ip.dst_ctx1) AND (ip.src_ctx1 = ip.dst_ctx0) AND (tcp.options.timestamp.tsecr_ctx1 = tcp.options.timestamp.tsval_ctx0) AND (tcp.len_ctx0 > 0) AND (tcp.len_ctx1 > 0)) -> (tcp.ack_ctx1 = (tcp.len_ctx0 + tcp.seq_ctx0))
MOD(ip.hdr_len_ctx2, 4) = 0
(tcp.window_size_scalefactor_ctx0 * tcp.window_size_value_ctx0) = tcp.window_size_ctx0
((ip.src_ctx1 = ip.dst_ctx2) AND (ip.src_ctx2 = ip.dst_ctx1) AND (tcp.len_ctx1 = 0) AND (tcp.options.timestamp.tsecr_ctx2 = tcp.options.timestamp.tsval_ctx1) AND (NOT ((tcp.flags_ctx1 = 1) OR (tcp.flags_ctx1 = 2) OR (tcp.flags_ctx1 = 17) OR (tcp.flags_ctx1 = 18)))) -> (tcp.ack_ctx2 = tcp.seq_ctx1)
((tcp.flags_ctx0 = 2) AND (tcp.flags_ctx1 = 18) AND (tcp.flags_ctx2 = 16) AND (tcp.options.timestamp.tsval_ctx0 > 0) AND (tcp.options.timestamp.tsval_ctx1 > 0)) -> ((tcp.options.timestamp.tsecr_ctx1 = tcp.options.timestamp.tsval_ctx0) AND (tcp.options.timestamp.tsecr_ctx2 = tcp.options.timestamp.tsval_ctx1))
MOD(ip.hdr_len_ctx0, 4) = 0
((ip.dst_ctx1 = ip.src_ctx0) AND (ip.src_ctx1 = ip.dst_ctx0) AND (tcp.flags_ctx0 = 24) AND (tcp.options.timestamp.tsval_ctx0 = tcp.options.timestamp.tsecr_ctx1)) -> ((tcp.flags_ctx1 = 4) OR (tcp.flags_ctx1 = 16) OR (tcp.flags_ctx1 = 17) OR (tcp.flags_ctx1 = 20) OR (tcp.flags_ctx1 = 24))
((ip.dst_ctx0 = ip.src_ctx1) AND (ip.src_ctx0 = ip.dst_ctx1)) -> ((tcp.dstport_ctx0 = tcp.srcport_ctx1) AND (tcp.srcport_ctx0 = tcp.dstport_ctx1))
((ip.dst_ctx0 = ip.dst_ctx1) AND (ip.src_ctx0 = ip.src_ctx1) AND (tcp.flags_ctx0 = tcp.flags_ctx1) AND (tcp.len_ctx0 = tcp.len_ctx1) AND (tcp.seq_ctx0 = tcp.seq_ctx1)) -> ((ip.dst_ctx0 = ip.dst_ctx1) AND (ip.src_ctx0 = ip.src_ctx1))
((ip.src_ctx0 = ip.dst_ctx1) AND (ip.src_ctx1 = ip.dst_ctx0) AND (tcp.len_ctx0 = 0) AND (tcp.options.timestamp.tsecr_ctx1 = tcp.options.timestamp.tsval_ctx0) AND ((tcp.flags_ctx0 = 1) OR (tcp.flags_ctx0 = 2) OR (tcp.flags_ctx0 = 17) OR (tcp.flags_ctx0 = 18))) -> (tcp.ack_ctx1 = (tcp.seq_ctx0 + 1))
(tcp.window_size_scalefactor_ctx2 * tcp.window_size_value_ctx2) = tcp.window_size_ctx2
((tcp.flags_ctx0 = 17) AND (tcp.options.timestamp.tsval_ctx0 = tcp.options.timestamp.tsecr_ctx1)) -> ((tcp.flags_ctx1 = 16) AND (tcp.ack_ctx1 = (tcp.seq_ctx0 + 1)))
((tcp.ack_ctx0 = tcp.seq_ctx1) AND (tcp.flags_ctx1 = 16) AND (tcp.len_ctx1 = 0)) -> (tcp.seq_ctx1 = tcp.ack_ctx0)
((ip.dst_ctx1 = ip.src_ctx0) AND (ip.src_ctx1 = ip.dst_ctx0) AND (tcp.flags_ctx0 = 2) AND (tcp.flags_ctx1 = 18) AND (tcp.flags_ctx2 = 16)) -> ((tcp.seq_ctx2 = tcp.ack_ctx1) AND (tcp.ack_ctx1 = (tcp.seq_ctx0 + 1)) AND (tcp.ack_ctx2 = (tcp.seq_ctx1 + 1)))
(tcp.window_size_scalefactor_ctx1 * tcp.window_size_value_ctx1) = tcp.window_size_ctx1
ip.len_ctx0 <= 1500
tcp.seq_ctx0 >= 0
tcp.window_size_scalefactor_ctx2 <= 512
tcp.hdr_len_ctx1 <= 52
tcp.ack_ctx2 >= 1
tcp.ack_ctx0 <= 25013410
ip.ttl_ctx1 >= 56
tcp.options.timestamp.tsval_ctx0 >= 565270055
ip.ttl_ctx2 >= 56
tcp.window_size_scalefactor_ctx1 <= 512
tcp.window_size_ctx2 >= 66880
tcp.window_size_scalefactor_ctx1 >= 1
tcp.window_size_value_ctx0 >= 2050
tcp.window_size_ctx0 <= 1049600
ip.hdr_len_ctx2 >= 20
tcp.options.timestamp.tsval_ctx2 >= 565270162
tcp.seq_ctx2 <= 25013410
tcp.window_size_value_ctx1 <= 65535
ip.hdr_len_ctx0 <= 20
tcp.window_size_value_ctx1 >= 2050
ip.len_ctx2 <= 1500
tcp.seq_ctx2 >= 1
ip.hdr_len_ctx1 <= 20
tcp.len_ctx1 >= 0
tcp.len_ctx0 >= 0
ip.len_ctx0 >= 52
tcp.window_size_value_ctx2 >= 2050
tcp.ack_ctx2 <= 25013411
ip.ttl_ctx1 <= 64
ip.ttl_ctx2 <= 64
tcp.hdr_len_ctx1 >= 32
tcp.len_ctx0 <= 1448
tcp.seq_ctx0 <= 25013410
tcp.ack_ctx1 >= 1
ip.ttl_ctx0 <= 64
ip.hdr_len_ctx0 >= 20
ip.ttl_ctx0 >= 56
tcp.seq_ctx1 <= 25013410
tcp.options.timestamp.tsecr_ctx0 <= 2516246074
tcp.window_size_scalefactor_ctx0 <= 512
tcp.window_size_ctx0 >= 65535
tcp.hdr_len_ctx0 >= 32
tcp.seq_ctx1 >= 0
tcp.len_ctx1 <= 1448
tcp.options.timestamp.tsval_ctx0 <= 2516246074
tcp.window_size_ctx1 <= 1049600
tcp.len_ctx2 >= 0
tcp.options.timestamp.tsval_ctx1 <= 2516246074
tcp.window_size_ctx2 <= 1049600
tcp.ack_ctx0 >= 0
tcp.hdr_len_ctx2 <= 52
tcp.window_size_value_ctx0 <= 65535
tcp.hdr_len_ctx0 <= 52
tcp.options.timestamp.tsval_ctx2 <= 2516246074
tcp.options.timestamp.tsecr_ctx1 <= 2516246074
tcp.options.timestamp.tsecr_ctx2 <= 2516246074
tcp.len_ctx2 <= 1448
ip.hdr_len_ctx1 >= 20
tcp.window_size_scalefactor_ctx2 >= 32
ip.hdr_len_ctx2 <= 20
tcp.options.timestamp.tsecr_ctx2 >= 565270162
ip.len_ctx1 <= 1500
tcp.options.timestamp.tsval_ctx1 >= 565270162
tcp.flags_ctx2 >= 0
tcp.window_size_scalefactor_ctx0 >= 1
tcp.flags_ctx0 <= 24
tcp.window_size_value_ctx2 <= 5068
tcp.ack_ctx1 <= 25013410
tcp.options.timestamp.tsecr_ctx1 >= 565270055
tcp.hdr_len_ctx2 >= 32
tcp.flags_ctx2 <= 24
tcp.flags_ctx0 >= 0
tcp.flags_ctx1 >= 0
ip.len_ctx2 >= 52
tcp.flags_ctx1 <= 24
ip.len_ctx1 >= 52
tcp.window_size_ctx1 >= 65535
tcp.options.timestamp.tsecr_ctx0 >= 0
