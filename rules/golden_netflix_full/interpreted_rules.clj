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
tcp.window_size_scalefactor_ctx1 <= tcp.window_size_scalefactor_ctx2
tcp.len_ctx1 != (tcp.hdr_len_ctx1 + tcp.hdr_len_ctx2)
tcp.ack_ctx0 != (tcp.seq_ctx0 + tcp.seq_ctx1)
tcp.window_size_ctx1 <= (tcp.window_size_scalefactor_ctx2 * tcp.window_size_value_ctx1)
tcp.hdr_len_ctx0 != (ip.hdr_len_ctx0 + tcp.hdr_len_ctx1)
ip.len_ctx0 = (ip.hdr_len_ctx0 + tcp.hdr_len_ctx2)
tcp.len_ctx2 != (tcp.len_ctx0 + tcp.len_ctx1)
tcp.window_size_ctx0 != (tcp.window_size_scalefactor_ctx1 * tcp.window_size_value_ctx0)
tcp.ack_ctx2 != (tcp.seq_ctx0 + tcp.seq_ctx2)
tcp.seq_ctx2 != (tcp.seq_ctx0 + tcp.seq_ctx1)
tcp.seq_ctx0 = (tcp.ack_ctx0 + tcp.seq_ctx1)
tcp.options.timestamp.tsval_ctx0 <= tcp.options.timestamp.tsecr_ctx2
tcp.hdr_len_ctx2 <= (tcp.hdr_len_ctx0 + tcp.len_ctx2)
tcp.seq_ctx0 != tcp.ack_ctx1
tcp.window_size_ctx0 = (tcp.window_size_scalefactor_ctx0 * tcp.window_size_value_ctx2)
ip.len_ctx2 = (ip.hdr_len_ctx0 + tcp.hdr_len_ctx0)
tcp.ack_ctx2 != (tcp.ack_ctx1 + tcp.seq_ctx1)
tcp.window_size_value_ctx0 != tcp.window_size_ctx0
ip.hdr_len_ctx0 != (ip.hdr_len_ctx2 + tcp.len_ctx0)
tcp.options.timestamp.tsecr_ctx1 = tcp.options.timestamp.tsecr_ctx2
tcp.hdr_len_ctx2 != (tcp.hdr_len_ctx0 + tcp.len_ctx1)
tcp.ack_ctx1 = (tcp.ack_ctx2 + tcp.seq_ctx0)
tcp.options.timestamp.tsecr_ctx0 <= tcp.options.timestamp.tsecr_ctx2
ip.len_ctx1 = (ip.hdr_len_ctx2 + tcp.hdr_len_ctx2)
ip.src_ctx1 = ip.src_ctx2
tcp.seq_ctx2 != (tcp.ack_ctx0 + tcp.ack_ctx1)
tcp.window_size_value_ctx1 > tcp.window_size_value_ctx2
tcp.flags_ctx0 = 2
ip.hdr_len_ctx2 != (ip.hdr_len_ctx1 + tcp.len_ctx1)
tcp.window_size_ctx2 != (tcp.window_size_scalefactor_ctx2 * tcp.window_size_value_ctx0)
tcp.window_size_ctx2 != (tcp.window_size_scalefactor_ctx2 + tcp.window_size_ctx1)
tcp.window_size_ctx0 <= (tcp.window_size_scalefactor_ctx1 * tcp.window_size_value_ctx0)
ip.hdr_len_ctx1 != (ip.hdr_len_ctx0 + tcp.len_ctx1)
tcp.hdr_len_ctx2 = (tcp.hdr_len_ctx1 + tcp.len_ctx0)
tcp.window_size_value_ctx0 != (tcp.window_size_scalefactor_ctx0 * tcp.window_size_ctx1)
ip.len_ctx1 != (tcp.hdr_len_ctx2 + tcp.len_ctx1)
tcp.window_size_ctx2 != (tcp.window_size_scalefactor_ctx1 * tcp.window_size_value_ctx0)
tcp.hdr_len_ctx2 <= 0
tcp.window_size_ctx1 = (tcp.window_size_scalefactor_ctx1 * tcp.window_size_ctx0)
ip.ttl_ctx0 != ip.ttl_ctx1
tcp.dstport_ctx0 = tcp.dstport_ctx2
tcp.hdr_len_ctx1 > 0
tcp.ack_ctx1 != (tcp.seq_ctx1 + tcp.seq_ctx2)
tcp.window_size_ctx2 = (tcp.window_size_scalefactor_ctx1 * tcp.window_size_value_ctx1)
ip.hdr_len_ctx0 != (ip.hdr_len_ctx2 + tcp.len_ctx1)
tcp.window_size_ctx2 <= (tcp.window_size_scalefactor_ctx0 * tcp.window_size_value_ctx2)
tcp.dstport_ctx0 = tcp.srcport_ctx1
ip.len_ctx2 <= (tcp.hdr_len_ctx1 + tcp.len_ctx2)
ip.len_ctx2 <= (ip.hdr_len_ctx2 + tcp.hdr_len_ctx2)
tcp.window_size_ctx2 > (tcp.window_size_scalefactor_ctx1 * tcp.window_size_value_ctx1)
tcp.window_size_ctx1 != (tcp.window_size_scalefactor_ctx0 * tcp.window_size_ctx2)
tcp.dstport_ctx0 != tcp.dstport_ctx2
tcp.options.timestamp.tsval_ctx0 != tcp.options.timestamp.tsecr_ctx2
ip.len_ctx1 > (ip.len_ctx0 + tcp.len_ctx0)
tcp.window_size_ctx1 <= (tcp.window_size_scalefactor_ctx1 * tcp.window_size_value_ctx0)
tcp.srcport_ctx0 != tcp.dstport_ctx1
ip.dst_ctx0 != ip.src_ctx2
tcp.flags_ctx0 != tcp.flags_ctx1
tcp.hdr_len_ctx1 != (tcp.hdr_len_ctx0 + tcp.len_ctx2)
tcp.seq_ctx2 = tcp.ack_ctx2
ip.len_ctx1 <= (ip.hdr_len_ctx1 + tcp.hdr_len_ctx0)
ip.len_ctx0 = (ip.len_ctx2 + tcp.len_ctx2)
tcp.window_size_value_ctx2 != (tcp.window_size_scalefactor_ctx0 * tcp.window_size_value_ctx1)
ip.len_ctx2 = (ip.hdr_len_ctx2 + tcp.hdr_len_ctx2)
tcp.ack_ctx1 != (tcp.ack_ctx0 + tcp.seq_ctx2)
ip.hdr_len_ctx2 != (ip.hdr_len_ctx0 + tcp.len_ctx1)
tcp.window_size_scalefactor_ctx1 = (tcp.window_size_scalefactor_ctx0 * tcp.window_size_scalefactor_ctx2)
ip.hdr_len_ctx2 = (ip.hdr_len_ctx1 + tcp.len_ctx1)
ip.len_ctx1 > (tcp.hdr_len_ctx0 + tcp.len_ctx1)
tcp.len_ctx2 > (tcp.hdr_len_ctx1 + tcp.hdr_len_ctx2)
tcp.window_size_ctx2 = (tcp.window_size_scalefactor_ctx2 + tcp.window_size_ctx0)
tcp.len_ctx0 > (tcp.hdr_len_ctx0 + tcp.hdr_len_ctx1)
tcp.ack_ctx2 = (tcp.seq_ctx1 + tcp.seq_ctx2)
tcp.window_size_ctx0 <= (tcp.window_size_scalefactor_ctx0 * tcp.window_size_value_ctx2)
tcp.seq_ctx2 = (tcp.ack_ctx1 + tcp.seq_ctx0)
tcp.window_size_ctx0 > tcp.window_size_ctx1
tcp.seq_ctx2 = (tcp.seq_ctx0 + tcp.seq_ctx1)
tcp.hdr_len_ctx2 != (ip.hdr_len_ctx1 + tcp.hdr_len_ctx1)
tcp.window_size_value_ctx0 = (tcp.window_size_scalefactor_ctx1 * tcp.window_size_value_ctx1)
tcp.window_size_ctx2 <= (tcp.window_size_scalefactor_ctx1 + tcp.window_size_ctx0)
tcp.options.timestamp.tsval_ctx0 <= tcp.options.timestamp.tsval_ctx1
tcp.window_size_ctx0 <= (tcp.window_size_scalefactor_ctx1 * tcp.window_size_value_ctx1)
ip.hdr_len_ctx0 != (ip.hdr_len_ctx1 + tcp.len_ctx0)
tcp.ack_ctx1 != tcp.ack_ctx2
tcp.seq_ctx1 = tcp.seq_ctx2
tcp.hdr_len_ctx1 > (tcp.hdr_len_ctx0 + tcp.len_ctx2)
ip.len_ctx2 != (ip.len_ctx1 + tcp.len_ctx2)
tcp.ack_ctx0 != tcp.seq_ctx2
tcp.len_ctx2 > (tcp.len_ctx0 + tcp.len_ctx1)
tcp.dstport_ctx0 != tcp.dstport_ctx1
tcp.len_ctx1 > (tcp.len_ctx0 + tcp.len_ctx2)
ip.len_ctx0 > (ip.hdr_len_ctx1 + tcp.hdr_len_ctx0)
tcp.options.timestamp.tsecr_ctx1 != tcp.options.timestamp.tsval_ctx2
ip.len_ctx2 = (ip.hdr_len_ctx0 + tcp.hdr_len_ctx2)
ip.len_ctx0 <= (ip.len_ctx2 + tcp.len_ctx0)
tcp.window_size_ctx0 != (tcp.window_size_scalefactor_ctx0 + tcp.window_size_ctx2)
tcp.len_ctx0 > 0
tcp.window_size_ctx1 > (tcp.window_size_scalefactor_ctx0 * tcp.window_size_value_ctx2)
ip.len_ctx2 = (tcp.hdr_len_ctx1 + tcp.len_ctx2)
tcp.window_size_ctx1 > (tcp.window_size_scalefactor_ctx0 + tcp.window_size_ctx0)
tcp.len_ctx1 != (tcp.hdr_len_ctx0 + tcp.hdr_len_ctx2)
ip.hdr_len_ctx0 = (ip.hdr_len_ctx2 + tcp.len_ctx0)
ip.hdr_len_ctx1 > 0
tcp.window_size_value_ctx0 > (tcp.window_size_scalefactor_ctx0 * tcp.window_size_value_ctx1)
tcp.window_size_value_ctx0 > tcp.window_size_value_ctx2
tcp.window_size_value_ctx2 <= (tcp.window_size_scalefactor_ctx2 + tcp.window_size_value_ctx1)
tcp.dstport_ctx1 = tcp.srcport_ctx2
tcp.options.timestamp.tsval_ctx1 <= (tcp.options.timestamp.tsecr_ctx0 + tcp.options.timestamp.tsecr_ctx2)
ip.len_ctx0 > (ip.hdr_len_ctx0 + tcp.hdr_len_ctx0)
tcp.seq_ctx2 = (tcp.seq_ctx0 + 1)
ip.len_ctx1 <= (ip.hdr_len_ctx1 + tcp.hdr_len_ctx2)
tcp.window_size_value_ctx1 > (tcp.window_size_scalefactor_ctx1 + tcp.window_size_value_ctx0)
tcp.window_size_ctx2 > (tcp.window_size_scalefactor_ctx1 + tcp.window_size_ctx1)
tcp.seq_ctx2 = (tcp.ack_ctx1 + tcp.seq_ctx1)
tcp.len_ctx2 <= (tcp.len_ctx0 + tcp.len_ctx1)
tcp.window_size_ctx2 > (tcp.window_size_scalefactor_ctx1 * tcp.window_size_value_ctx0)
tcp.options.timestamp.tsecr_ctx1 != (tcp.options.timestamp.tsecr_ctx0 + tcp.options.timestamp.tsval_ctx0)
tcp.srcport_ctx0 != tcp.dstport_ctx2
ip.hdr_len_ctx2 != (ip.hdr_len_ctx0 + tcp.len_ctx2)
tcp.flags_ctx0 = tcp.flags_ctx1
ip.len_ctx2 > (tcp.hdr_len_ctx1 + tcp.len_ctx0)
tcp.window_size_value_ctx1 = tcp.window_size_value_ctx2
tcp.window_size_ctx1 != (tcp.window_size_scalefactor_ctx0 * tcp.window_size_value_ctx2)
ip.len_ctx1 = (tcp.hdr_len_ctx0 + tcp.hdr_len_ctx2)
tcp.window_size_value_ctx0 <= tcp.window_size_value_ctx2
tcp.window_size_value_ctx1 <= (tcp.window_size_scalefactor_ctx0 * tcp.window_size_value_ctx2)
tcp.dstport_ctx1 != tcp.dstport_ctx2
ip.len_ctx2 != (ip.len_ctx0 + tcp.len_ctx2)
tcp.window_size_ctx0 != (tcp.window_size_scalefactor_ctx1 * tcp.window_size_value_ctx1)
tcp.window_size_ctx0 != (tcp.window_size_scalefactor_ctx1 * tcp.window_size_ctx1)
ip.len_ctx2 != (ip.hdr_len_ctx1 + tcp.hdr_len_ctx0)
tcp.len_ctx0 = (tcp.hdr_len_ctx0 + tcp.hdr_len_ctx2)
tcp.hdr_len_ctx1 = (tcp.hdr_len_ctx0 + tcp.len_ctx2)
tcp.len_ctx0 <= (tcp.hdr_len_ctx0 + tcp.hdr_len_ctx1)
ip.len_ctx0 = (ip.len_ctx1 + tcp.len_ctx2)
tcp.options.timestamp.tsecr_ctx0 = tcp.options.timestamp.tsval_ctx1
ip.len_ctx2 != (tcp.hdr_len_ctx1 + tcp.len_ctx2)
tcp.srcport_ctx0 = tcp.srcport_ctx1
tcp.window_size_value_ctx1 = (tcp.window_size_scalefactor_ctx1 * tcp.window_size_ctx0)
tcp.hdr_len_ctx2 != (ip.hdr_len_ctx0 + tcp.hdr_len_ctx1)
ip.len_ctx1 = (ip.len_ctx2 + tcp.len_ctx1)
ip.len_ctx2 != (ip.hdr_len_ctx1 + tcp.hdr_len_ctx1)
tcp.seq_ctx0 > 1
tcp.window_size_ctx0 <= (tcp.window_size_scalefactor_ctx2 * tcp.window_size_value_ctx2)
tcp.hdr_len_ctx0 != (tcp.hdr_len_ctx2 + tcp.len_ctx1)
tcp.seq_ctx2 <= 1
tcp.window_size_value_ctx1 != (tcp.window_size_scalefactor_ctx1 * tcp.window_size_ctx1)
tcp.hdr_len_ctx2 = (tcp.hdr_len_ctx1 + tcp.len_ctx1)
tcp.flags_ctx1 != tcp.flags_ctx2
tcp.options.timestamp.tsecr_ctx0 > tcp.options.timestamp.tsecr_ctx2
ip.len_ctx1 <= (ip.len_ctx2 + tcp.len_ctx0)
ip.len_ctx1 != (ip.len_ctx0 + tcp.len_ctx2)
ip.hdr_len_ctx0 = (ip.hdr_len_ctx2 + tcp.len_ctx1)
tcp.seq_ctx1 = (tcp.seq_ctx0 + tcp.seq_ctx2)
tcp.hdr_len_ctx0 > (tcp.hdr_len_ctx1 + tcp.len_ctx2)
tcp.options.timestamp.tsval_ctx0 != tcp.options.timestamp.tsval_ctx2
tcp.window_size_ctx0 > (tcp.window_size_scalefactor_ctx0 + tcp.window_size_ctx2)
ip.len_ctx2 <= (ip.len_ctx1 + tcp.len_ctx0)
tcp.hdr_len_ctx0 > 0
tcp.window_size_scalefactor_ctx0 <= tcp.window_size_scalefactor_ctx2
ip.len_ctx1 <= (ip.hdr_len_ctx0 + tcp.hdr_len_ctx1)
tcp.window_size_value_ctx0 = (tcp.window_size_scalefactor_ctx0 * tcp.window_size_value_ctx1)
tcp.window_size_value_ctx0 = tcp.window_size_ctx1
tcp.seq_ctx0 != tcp.ack_ctx0
ip.len_ctx0 > (ip.hdr_len_ctx1 + tcp.hdr_len_ctx2)
tcp.flags_ctx2 != 17
tcp.seq_ctx2 = (tcp.ack_ctx2 + tcp.seq_ctx1)
tcp.len_ctx0 <= 0
tcp.len_ctx2 = (tcp.len_ctx0 + tcp.len_ctx1)
ip.len_ctx0 != (tcp.hdr_len_ctx1 + tcp.len_ctx2)
tcp.window_size_value_ctx0 = tcp.window_size_value_ctx1
ip.len_ctx2 = (ip.hdr_len_ctx2 + tcp.hdr_len_ctx1)
tcp.options.timestamp.tsecr_ctx1 <= tcp.options.timestamp.tsval_ctx2
tcp.seq_ctx1 = tcp.ack_ctx2
tcp.seq_ctx1 > 1
ip.hdr_len_ctx0 <= 0
ip.src_ctx0 = ip.dst_ctx2
ip.len_ctx2 > (ip.hdr_len_ctx0 + tcp.hdr_len_ctx2)
tcp.window_size_ctx1 > (tcp.window_size_scalefactor_ctx1 + tcp.window_size_ctx0)
tcp.window_size_ctx1 > (tcp.window_size_scalefactor_ctx1 * tcp.window_size_value_ctx2)
ip.len_ctx0 != (tcp.hdr_len_ctx1 + tcp.hdr_len_ctx2)
ip.len_ctx1 != (ip.hdr_len_ctx1 + tcp.hdr_len_ctx2)
ip.len_ctx1 != ip.len_ctx2
ip.dst_ctx0 != ip.dst_ctx2
ip.len_ctx1 != (tcp.hdr_len_ctx0 + tcp.hdr_len_ctx2)
tcp.flags_ctx1 != 17
tcp.window_size_ctx2 <= (tcp.window_size_scalefactor_ctx0 * tcp.window_size_ctx1)
tcp.window_size_ctx1 <= tcp.window_size_ctx2
ip.src_ctx0 != ip.dst_ctx2
ip.len_ctx0 = (ip.len_ctx1 + tcp.len_ctx0)
tcp.window_size_ctx2 = (tcp.window_size_scalefactor_ctx1 * tcp.window_size_value_ctx0)
ip.len_ctx0 = (ip.hdr_len_ctx1 + tcp.hdr_len_ctx1)
tcp.srcport_ctx1 != tcp.srcport_ctx2
tcp.window_size_ctx2 = (tcp.window_size_scalefactor_ctx1 + tcp.window_size_ctx1)
ip.len_ctx0 <= (ip.hdr_len_ctx0 + tcp.hdr_len_ctx1)
tcp.hdr_len_ctx2 > (tcp.hdr_len_ctx1 + tcp.len_ctx0)
tcp.window_size_value_ctx1 != (tcp.window_size_scalefactor_ctx0 * tcp.window_size_ctx0)
tcp.hdr_len_ctx0 > tcp.hdr_len_ctx2
ip.len_ctx2 > (ip.len_ctx0 + tcp.len_ctx0)
tcp.window_size_ctx0 > tcp.window_size_value_ctx1
tcp.ack_ctx1 != (tcp.ack_ctx0 + tcp.ack_ctx2)
tcp.window_size_ctx1 != (tcp.window_size_scalefactor_ctx1 * tcp.window_size_value_ctx2)
ip.len_ctx1 = (tcp.hdr_len_ctx2 + tcp.len_ctx1)
tcp.window_size_ctx2 != (tcp.window_size_scalefactor_ctx1 + tcp.window_size_ctx0)
ip.src_ctx1 != ip.dst_ctx2
ip.len_ctx1 = (ip.hdr_len_ctx2 + tcp.hdr_len_ctx1)
tcp.ack_ctx0 = (tcp.seq_ctx0 + tcp.seq_ctx1)
ip.hdr_len_ctx2 > 0
tcp.window_size_scalefactor_ctx2 > (tcp.window_size_scalefactor_ctx0 * tcp.window_size_scalefactor_ctx1)
tcp.window_size_value_ctx1 = (tcp.window_size_scalefactor_ctx0 * tcp.window_size_ctx1)
tcp.hdr_len_ctx0 <= (tcp.hdr_len_ctx1 + tcp.len_ctx2)
tcp.len_ctx0 != (tcp.len_ctx1 + tcp.len_ctx2)
tcp.len_ctx0 <= tcp.len_ctx1
ip.hdr_len_ctx0 != (ip.hdr_len_ctx2 + tcp.len_ctx2)
tcp.window_size_ctx1 <= (tcp.window_size_scalefactor_ctx1 + tcp.window_size_ctx0)
tcp.options.timestamp.tsval_ctx0 = (tcp.options.timestamp.tsecr_ctx0 + tcp.options.timestamp.tsecr_ctx1)
ip.len_ctx1 <= (ip.len_ctx2 + tcp.len_ctx2)
ip.len_ctx0 > (tcp.hdr_len_ctx1 + tcp.len_ctx0)
tcp.hdr_len_ctx0 = tcp.hdr_len_ctx2
tcp.ack_ctx0 = (tcp.seq_ctx0 + 1)
tcp.window_size_ctx1 = (tcp.window_size_scalefactor_ctx0 * tcp.window_size_value_ctx2)
tcp.flags_ctx2 != 24
tcp.window_size_ctx0 = (tcp.window_size_scalefactor_ctx1 * tcp.window_size_value_ctx1)
tcp.hdr_len_ctx0 <= tcp.hdr_len_ctx1
tcp.window_size_ctx2 <= (tcp.window_size_scalefactor_ctx1 + tcp.window_size_ctx1)
ip.len_ctx0 = (ip.hdr_len_ctx2 + tcp.hdr_len_ctx2)
tcp.window_size_ctx2 > (tcp.window_size_scalefactor_ctx0 + tcp.window_size_ctx0)
tcp.window_size_ctx1 = (tcp.window_size_scalefactor_ctx0 * tcp.window_size_value_ctx1)
tcp.window_size_ctx1 <= (tcp.window_size_scalefactor_ctx0 * tcp.window_size_ctx0)
tcp.seq_ctx2 != (tcp.ack_ctx0 + tcp.ack_ctx2)
tcp.ack_ctx2 = (tcp.seq_ctx1 + 1)
tcp.window_size_ctx1 != (tcp.window_size_scalefactor_ctx2 * tcp.window_size_value_ctx2)
tcp.flags_ctx0 != 18
ip.len_ctx2 <= (ip.hdr_len_ctx0 + tcp.hdr_len_ctx1)
tcp.hdr_len_ctx1 > (tcp.hdr_len_ctx2 + tcp.len_ctx1)
tcp.options.timestamp.tsecr_ctx0 != tcp.options.timestamp.tsval_ctx1
tcp.window_size_ctx1 = (tcp.window_size_scalefactor_ctx1 + tcp.window_size_ctx0)
ip.len_ctx2 <= 0
tcp.srcport_ctx1 = tcp.srcport_ctx2
tcp.window_size_value_ctx0 != tcp.window_size_value_ctx1
tcp.window_size_ctx2 > (tcp.window_size_scalefactor_ctx2 * tcp.window_size_value_ctx0)
tcp.window_size_ctx1 > (tcp.window_size_scalefactor_ctx2 * tcp.window_size_value_ctx1)
tcp.window_size_ctx0 > (tcp.window_size_scalefactor_ctx2 * tcp.window_size_value_ctx1)
tcp.window_size_value_ctx1 != (tcp.window_size_scalefactor_ctx1 * tcp.window_size_ctx0)
tcp.window_size_ctx0 > (tcp.window_size_scalefactor_ctx0 * tcp.window_size_value_ctx1)
tcp.window_size_ctx2 <= (tcp.window_size_scalefactor_ctx2 * tcp.window_size_value_ctx0)
tcp.window_size_value_ctx2 > (tcp.window_size_scalefactor_ctx1 + tcp.window_size_value_ctx1)
tcp.window_size_ctx0 != tcp.window_size_ctx1
tcp.window_size_ctx2 <= (tcp.window_size_scalefactor_ctx1 * tcp.window_size_value_ctx2)
ip.len_ctx2 <= (ip.len_ctx0 + tcp.len_ctx0)
tcp.len_ctx0 > (tcp.hdr_len_ctx1 + tcp.hdr_len_ctx2)
tcp.window_size_ctx2 > (tcp.window_size_scalefactor_ctx0 * tcp.window_size_value_ctx1)
tcp.window_size_ctx1 = (tcp.window_size_scalefactor_ctx2 * tcp.window_size_value_ctx2)
tcp.window_size_ctx1 = (tcp.window_size_scalefactor_ctx2 * tcp.window_size_value_ctx1)
tcp.seq_ctx2 != (tcp.ack_ctx2 + tcp.seq_ctx1)
tcp.hdr_len_ctx1 > (tcp.hdr_len_ctx2 + tcp.len_ctx2)
tcp.ack_ctx0 != tcp.ack_ctx2
tcp.hdr_len_ctx2 > 0
ip.len_ctx0 != (ip.hdr_len_ctx2 + tcp.hdr_len_ctx0)
ip.len_ctx1 != (ip.len_ctx0 + tcp.len_ctx1)
tcp.ack_ctx0 != (tcp.seq_ctx0 + tcp.seq_ctx2)
ip.hdr_len_ctx0 != (ip.hdr_len_ctx1 + tcp.len_ctx1)
tcp.seq_ctx0 = tcp.seq_ctx1
tcp.ack_ctx2 != (tcp.seq_ctx1 + 1)
ip.len_ctx0 <= (ip.len_ctx1 + tcp.len_ctx0)
ip.hdr_len_ctx1 = (ip.hdr_len_ctx2 + tcp.len_ctx2)
ip.len_ctx2 > (ip.hdr_len_ctx2 + tcp.hdr_len_ctx2)
tcp.hdr_len_ctx1 != (tcp.hdr_len_ctx2 + tcp.len_ctx0)
ip.len_ctx1 = (ip.len_ctx2 + tcp.len_ctx2)
tcp.options.timestamp.tsecr_ctx0 > tcp.options.timestamp.tsval_ctx2
tcp.options.timestamp.tsecr_ctx2 > (tcp.options.timestamp.tsecr_ctx0 + tcp.options.timestamp.tsval_ctx1)
tcp.window_size_ctx1 = (tcp.window_size_scalefactor_ctx0 + tcp.window_size_ctx0)
tcp.hdr_len_ctx2 = (tcp.hdr_len_ctx1 + tcp.len_ctx2)
tcp.window_size_scalefactor_ctx0 > tcp.window_size_scalefactor_ctx2
ip.len_ctx0 > (ip.hdr_len_ctx2 + tcp.hdr_len_ctx1)
tcp.seq_ctx1 = tcp.ack_ctx1
tcp.window_size_ctx2 = (tcp.window_size_scalefactor_ctx0 * tcp.window_size_value_ctx2)
ip.len_ctx2 = (ip.len_ctx1 + tcp.len_ctx1)
tcp.len_ctx1 > 0
ip.len_ctx0 <= (ip.hdr_len_ctx0 + tcp.hdr_len_ctx2)
tcp.ack_ctx0 = (tcp.ack_ctx1 + tcp.seq_ctx0)
tcp.window_size_value_ctx1 != (tcp.window_size_scalefactor_ctx0 * tcp.window_size_ctx1)
tcp.window_size_value_ctx1 > (tcp.window_size_scalefactor_ctx0 + tcp.window_size_value_ctx0)
tcp.ack_ctx0 = (tcp.seq_ctx0 + tcp.seq_ctx2)
tcp.ack_ctx1 = (tcp.ack_ctx0 + tcp.ack_ctx2)
ip.len_ctx0 <= (ip.hdr_len_ctx1 + tcp.hdr_len_ctx2)
ip.hdr_len_ctx2 = (ip.hdr_len_ctx0 + tcp.len_ctx1)
ip.len_ctx0 <= (ip.hdr_len_ctx2 + tcp.hdr_len_ctx2)
ip.len_ctx1 <= (ip.hdr_len_ctx2 + tcp.hdr_len_ctx1)
ip.hdr_len_ctx1 = (ip.hdr_len_ctx2 + tcp.len_ctx0)
tcp.window_size_value_ctx1 = (tcp.window_size_scalefactor_ctx0 * tcp.window_size_ctx0)
tcp.flags_ctx1 = 24
ip.len_ctx0 <= (ip.len_ctx1 + tcp.len_ctx2)
ip.len_ctx0 = (ip.hdr_len_ctx2 + tcp.hdr_len_ctx0)
tcp.seq_ctx0 != tcp.seq_ctx1
ip.len_ctx0 = (ip.hdr_len_ctx1 + tcp.hdr_len_ctx2)
tcp.seq_ctx1 != tcp.ack_ctx1
tcp.hdr_len_ctx0 > (tcp.hdr_len_ctx1 + tcp.len_ctx0)
ip.hdr_len_ctx2 != (ip.hdr_len_ctx1 + tcp.len_ctx2)
tcp.options.timestamp.tsval_ctx1 = tcp.options.timestamp.tsecr_ctx2
tcp.window_size_value_ctx1 != tcp.window_size_ctx1
tcp.options.timestamp.tsval_ctx1 != tcp.options.timestamp.tsecr_ctx2
tcp.ack_ctx1 = (tcp.seq_ctx0 + tcp.seq_ctx1)
tcp.seq_ctx1 != (tcp.seq_ctx0 + 1)
ip.len_ctx1 > (ip.hdr_len_ctx0 + tcp.hdr_len_ctx1)
tcp.options.timestamp.tsecr_ctx0 <= tcp.options.timestamp.tsecr_ctx1
ip.len_ctx0 <= ip.len_ctx2
ip.hdr_len_ctx1 <= 0
tcp.options.timestamp.tsecr_ctx1 > tcp.options.timestamp.tsval_ctx2
tcp.hdr_len_ctx0 <= (tcp.hdr_len_ctx2 + tcp.len_ctx0)
tcp.options.timestamp.tsecr_ctx0 != tcp.options.timestamp.tsecr_ctx1
ip.len_ctx2 <= (tcp.hdr_len_ctx0 + tcp.hdr_len_ctx1)
tcp.window_size_ctx0 > (tcp.window_size_scalefactor_ctx1 * tcp.window_size_value_ctx2)
tcp.dstport_ctx0 != tcp.srcport_ctx2
tcp.hdr_len_ctx2 <= (tcp.hdr_len_ctx0 + tcp.len_ctx1)
ip.len_ctx1 <= (ip.hdr_len_ctx0 + tcp.hdr_len_ctx2)
tcp.window_size_value_ctx0 != (tcp.window_size_scalefactor_ctx0 * tcp.window_size_ctx0)
ip.len_ctx2 <= (ip.hdr_len_ctx1 + tcp.hdr_len_ctx0)
tcp.flags_ctx0 != 2
tcp.len_ctx2 > (tcp.hdr_len_ctx0 + tcp.hdr_len_ctx2)
tcp.len_ctx1 = (tcp.hdr_len_ctx0 + tcp.hdr_len_ctx1)
tcp.srcport_ctx1 = tcp.dstport_ctx2
ip.len_ctx0 != ip.len_ctx1
ip.len_ctx2 <= (ip.len_ctx0 + tcp.len_ctx1)
ip.len_ctx0 <= ip.len_ctx1
tcp.window_size_value_ctx1 <= tcp.window_size_value_ctx2
tcp.window_size_value_ctx1 != tcp.window_size_value_ctx2
tcp.window_size_ctx1 = (tcp.window_size_scalefactor_ctx1 * tcp.window_size_value_ctx2)
ip.dst_ctx0 != ip.dst_ctx1
tcp.seq_ctx1 != (tcp.ack_ctx2 + tcp.seq_ctx0)
tcp.flags_ctx1 = 16
tcp.hdr_len_ctx2 != (tcp.hdr_len_ctx1 + tcp.len_ctx0)
tcp.hdr_len_ctx0 = (ip.hdr_len_ctx1 + tcp.hdr_len_ctx1)
tcp.options.timestamp.tsval_ctx0 > tcp.options.timestamp.tsval_ctx2
ip.len_ctx1 <= (tcp.hdr_len_ctx0 + tcp.len_ctx1)
ip.len_ctx1 = (ip.len_ctx0 + tcp.len_ctx0)
tcp.ack_ctx0 = tcp.ack_ctx1
tcp.window_size_value_ctx1 != (tcp.window_size_scalefactor_ctx1 + tcp.window_size_value_ctx0)
tcp.window_size_ctx2 <= (tcp.window_size_scalefactor_ctx1 * tcp.window_size_value_ctx1)
tcp.window_size_ctx0 != (tcp.window_size_scalefactor_ctx2 * tcp.window_size_value_ctx0)
tcp.window_size_ctx1 != (tcp.window_size_scalefactor_ctx1 + tcp.window_size_ctx0)
tcp.flags_ctx0 != 24
tcp.ack_ctx1 = tcp.seq_ctx2
tcp.hdr_len_ctx2 <= (tcp.hdr_len_ctx1 + tcp.len_ctx0)
tcp.options.timestamp.tsval_ctx0 = tcp.options.timestamp.tsecr_ctx1
tcp.len_ctx0 != tcp.len_ctx2
tcp.ack_ctx0 > 1
ip.len_ctx2 > (ip.len_ctx1 + tcp.len_ctx1)
tcp.hdr_len_ctx1 != (tcp.hdr_len_ctx0 + tcp.len_ctx1)
tcp.hdr_len_ctx1 <= (tcp.hdr_len_ctx2 + tcp.len_ctx2)
tcp.window_size_ctx0 != (tcp.window_size_scalefactor_ctx2 * tcp.window_size_value_ctx1)
tcp.ack_ctx2 != (tcp.seq_ctx0 + 1)
tcp.len_ctx1 != (tcp.len_ctx0 + tcp.len_ctx2)
tcp.window_size_ctx0 <= tcp.window_size_ctx1
tcp.window_size_ctx0 != (tcp.window_size_scalefactor_ctx2 + tcp.window_size_ctx2)
ip.hdr_len_ctx2 = (ip.hdr_len_ctx1 + tcp.len_ctx2)
tcp.ack_ctx1 <= 1
ip.len_ctx0 != (ip.hdr_len_ctx2 + tcp.hdr_len_ctx1)
tcp.hdr_len_ctx0 = (tcp.hdr_len_ctx2 + tcp.len_ctx1)
ip.ttl_ctx0 > ip.ttl_ctx1
ip.len_ctx0 <= (tcp.hdr_len_ctx1 + tcp.len_ctx2)
tcp.window_size_ctx2 != (tcp.window_size_scalefactor_ctx1 + tcp.window_size_ctx1)
ip.len_ctx2 > (ip.hdr_len_ctx0 + tcp.hdr_len_ctx1)
tcp.window_size_ctx2 <= (tcp.window_size_scalefactor_ctx0 + tcp.window_size_ctx0)
tcp.flags_ctx0 = 24
tcp.hdr_len_ctx2 != (tcp.hdr_len_ctx0 + tcp.len_ctx0)
tcp.options.timestamp.tsval_ctx0 <= (tcp.options.timestamp.tsecr_ctx0 + tcp.options.timestamp.tsecr_ctx1)
tcp.window_size_ctx0 != (tcp.window_size_scalefactor_ctx2 * tcp.window_size_value_ctx2)
tcp.window_size_ctx1 <= (tcp.window_size_scalefactor_ctx0 * tcp.window_size_value_ctx2)
ip.hdr_len_ctx0 = (ip.hdr_len_ctx2 + tcp.len_ctx2)
ip.hdr_len_ctx0 = (ip.hdr_len_ctx1 + tcp.len_ctx2)
tcp.srcport_ctx0 != tcp.srcport_ctx2
tcp.len_ctx1 = tcp.len_ctx2
ip.len_ctx1 <= (ip.len_ctx0 + tcp.len_ctx0)
ip.len_ctx2 > (tcp.hdr_len_ctx0 + tcp.hdr_len_ctx1)
ip.len_ctx2 = (ip.hdr_len_ctx2 + tcp.hdr_len_ctx0)
tcp.options.timestamp.tsval_ctx0 = tcp.options.timestamp.tsecr_ctx2
tcp.seq_ctx1 != tcp.ack_ctx2
tcp.len_ctx0 > tcp.len_ctx2
tcp.window_size_value_ctx2 = (tcp.window_size_scalefactor_ctx0 * tcp.window_size_value_ctx1)
ip.hdr_len_ctx2 = (ip.hdr_len_ctx1 + tcp.len_ctx0)
tcp.seq_ctx1 = (tcp.ack_ctx2 + tcp.seq_ctx0)
ip.len_ctx0 = ip.len_ctx1
ip.len_ctx2 = (ip.hdr_len_ctx1 + tcp.hdr_len_ctx1)
tcp.window_size_value_ctx1 = tcp.window_size_ctx1
tcp.window_size_ctx1 != (tcp.window_size_scalefactor_ctx0 * tcp.window_size_ctx0)
tcp.window_size_ctx2 > (tcp.window_size_scalefactor_ctx2 + tcp.window_size_ctx1)
tcp.ack_ctx1 = tcp.ack_ctx2
tcp.window_size_ctx1 != (tcp.window_size_scalefactor_ctx1 * tcp.window_size_ctx0)
ip.hdr_len_ctx2 != (ip.hdr_len_ctx0 + tcp.len_ctx0)
tcp.ack_ctx2 = (tcp.seq_ctx0 + tcp.seq_ctx2)
tcp.hdr_len_ctx2 = (tcp.hdr_len_ctx0 + tcp.len_ctx2)
ip.hdr_len_ctx1 != (ip.hdr_len_ctx0 + tcp.len_ctx0)
tcp.hdr_len_ctx0 <= 0
ip.len_ctx0 <= (tcp.hdr_len_ctx1 + tcp.len_ctx0)
tcp.seq_ctx2 != (tcp.ack_ctx1 + tcp.seq_ctx1)
ip.len_ctx2 = (tcp.hdr_len_ctx0 + tcp.hdr_len_ctx1)
ip.len_ctx1 = (ip.hdr_len_ctx1 + tcp.hdr_len_ctx1)
tcp.window_size_ctx2 = (tcp.window_size_scalefactor_ctx0 * tcp.window_size_ctx1)
tcp.window_size_value_ctx1 != (tcp.window_size_scalefactor_ctx1 * tcp.window_size_value_ctx0)
tcp.len_ctx1 > tcp.len_ctx2
tcp.seq_ctx2 > 1
tcp.hdr_len_ctx0 <= (tcp.hdr_len_ctx2 + tcp.len_ctx2)
tcp.options.timestamp.tsecr_ctx0 = tcp.options.timestamp.tsecr_ctx1
tcp.window_size_ctx2 != (tcp.window_size_scalefactor_ctx1 * tcp.window_size_value_ctx2)
ip.len_ctx0 != (tcp.hdr_len_ctx1 + tcp.len_ctx0)
tcp.window_size_ctx2 <= (tcp.window_size_scalefactor_ctx1 * tcp.window_size_value_ctx0)
ip.len_ctx2 = (ip.hdr_len_ctx1 + tcp.hdr_len_ctx0)
tcp.seq_ctx2 != (tcp.seq_ctx0 + 1)
tcp.hdr_len_ctx1 != (ip.hdr_len_ctx2 + tcp.hdr_len_ctx0)
tcp.srcport_ctx0 != tcp.srcport_ctx1
ip.len_ctx1 <= (ip.hdr_len_ctx2 + tcp.hdr_len_ctx2)
tcp.window_size_ctx0 <= (tcp.window_size_scalefactor_ctx2 + tcp.window_size_ctx2)
tcp.window_size_ctx0 = (tcp.window_size_scalefactor_ctx2 * tcp.window_size_value_ctx1)
tcp.hdr_len_ctx2 = (tcp.hdr_len_ctx0 + tcp.len_ctx1)
tcp.flags_ctx2 = 16
tcp.hdr_len_ctx2 > (tcp.hdr_len_ctx0 + tcp.len_ctx2)
ip.len_ctx1 != (ip.hdr_len_ctx0 + tcp.hdr_len_ctx1)
tcp.hdr_len_ctx2 != (ip.hdr_len_ctx2 + tcp.hdr_len_ctx1)
tcp.ack_ctx2 <= 1
tcp.window_size_ctx1 != tcp.window_size_ctx2
ip.len_ctx1 = (ip.len_ctx0 + tcp.len_ctx1)
tcp.window_size_ctx1 = (tcp.window_size_scalefactor_ctx0 * tcp.window_size_value_ctx0)
ip.len_ctx1 != (ip.hdr_len_ctx2 + tcp.hdr_len_ctx1)
ip.len_ctx2 = (ip.hdr_len_ctx0 + tcp.hdr_len_ctx1)
tcp.options.timestamp.tsecr_ctx1 = tcp.options.timestamp.tsval_ctx2
ip.len_ctx1 <= 0
tcp.hdr_len_ctx2 > (tcp.hdr_len_ctx0 + tcp.len_ctx0)
tcp.window_size_ctx2 <= (tcp.window_size_scalefactor_ctx0 * tcp.window_size_value_ctx0)
ip.len_ctx0 != (ip.len_ctx1 + tcp.len_ctx0)
tcp.hdr_len_ctx1 = (tcp.hdr_len_ctx2 + tcp.len_ctx0)
ip.len_ctx1 = (ip.hdr_len_ctx0 + tcp.hdr_len_ctx2)
tcp.window_size_ctx1 <= (tcp.window_size_scalefactor_ctx1 * tcp.window_size_value_ctx2)
tcp.window_size_scalefactor_ctx0 <= tcp.window_size_scalefactor_ctx1
tcp.ack_ctx1 = (tcp.seq_ctx1 + tcp.seq_ctx2)
ip.len_ctx1 > (ip.len_ctx2 + tcp.len_ctx1)
tcp.seq_ctx1 != (tcp.seq_ctx0 + tcp.seq_ctx2)
tcp.len_ctx1 > (tcp.hdr_len_ctx0 + tcp.hdr_len_ctx2)
tcp.len_ctx2 != (tcp.hdr_len_ctx1 + tcp.hdr_len_ctx2)
tcp.len_ctx2 != (tcp.hdr_len_ctx0 + tcp.hdr_len_ctx2)
tcp.ack_ctx2 = (tcp.ack_ctx0 + tcp.seq_ctx2)
tcp.options.timestamp.tsval_ctx0 = tcp.options.timestamp.tsval_ctx1
tcp.window_size_ctx0 <= (tcp.window_size_scalefactor_ctx2 * tcp.window_size_value_ctx0)
ip.len_ctx2 <= (ip.hdr_len_ctx2 + tcp.hdr_len_ctx0)
tcp.len_ctx0 != tcp.len_ctx1
ip.len_ctx0 = (ip.hdr_len_ctx2 + tcp.hdr_len_ctx1)
ip.ttl_ctx0 = ip.ttl_ctx1
tcp.window_size_ctx2 = (tcp.window_size_scalefactor_ctx1 * tcp.window_size_value_ctx2)
ip.len_ctx1 > (ip.hdr_len_ctx1 + tcp.hdr_len_ctx2)
tcp.window_size_ctx0 > tcp.window_size_ctx2
tcp.window_size_value_ctx0 != (tcp.window_size_scalefactor_ctx1 * tcp.window_size_ctx1)
ip.len_ctx2 = (ip.len_ctx0 + tcp.len_ctx0)
tcp.window_size_ctx1 > (tcp.window_size_scalefactor_ctx2 * tcp.window_size_value_ctx0)
ip.len_ctx1 = (tcp.hdr_len_ctx0 + tcp.len_ctx1)
tcp.seq_ctx0 != tcp.ack_ctx2
ip.len_ctx2 <= (ip.hdr_len_ctx0 + tcp.hdr_len_ctx2)
tcp.hdr_len_ctx1 = (ip.hdr_len_ctx2 + tcp.hdr_len_ctx2)
tcp.window_size_ctx0 > (tcp.window_size_scalefactor_ctx1 * tcp.window_size_value_ctx1)
tcp.window_size_ctx0 = (tcp.window_size_scalefactor_ctx0 + tcp.window_size_ctx2)
tcp.ack_ctx2 != (tcp.seq_ctx0 + tcp.seq_ctx1)
tcp.len_ctx2 = (tcp.hdr_len_ctx0 + tcp.hdr_len_ctx2)
tcp.window_size_value_ctx1 != (tcp.window_size_scalefactor_ctx0 + tcp.window_size_value_ctx0)
tcp.window_size_ctx2 = (tcp.window_size_scalefactor_ctx2 * tcp.window_size_value_ctx0)
ip.len_ctx0 > 0
tcp.window_size_scalefactor_ctx0 > tcp.window_size_scalefactor_ctx1
tcp.ack_ctx1 = (tcp.ack_ctx0 + tcp.seq_ctx2)
ip.len_ctx0 != (ip.len_ctx1 + tcp.len_ctx2)
tcp.hdr_len_ctx2 <= (tcp.hdr_len_ctx1 + tcp.len_ctx2)
tcp.hdr_len_ctx1 = tcp.hdr_len_ctx2
tcp.seq_ctx1 != (tcp.ack_ctx0 + tcp.seq_ctx0)
tcp.hdr_len_ctx1 = (tcp.hdr_len_ctx2 + tcp.len_ctx1)
ip.len_ctx0 = (tcp.hdr_len_ctx1 + tcp.len_ctx0)
tcp.hdr_len_ctx1 <= (tcp.hdr_len_ctx2 + tcp.len_ctx1)
tcp.hdr_len_ctx0 <= (tcp.hdr_len_ctx2 + tcp.len_ctx1)
ip.ttl_ctx1 > ip.ttl_ctx2
tcp.len_ctx1 <= (tcp.hdr_len_ctx1 + tcp.hdr_len_ctx2)
tcp.len_ctx1 != tcp.len_ctx2
tcp.window_size_ctx1 <= (tcp.window_size_scalefactor_ctx2 * tcp.window_size_value_ctx0)
ip.len_ctx0 = (tcp.hdr_len_ctx1 + tcp.len_ctx2)
tcp.flags_ctx0 = 16
tcp.window_size_scalefactor_ctx2 != (tcp.window_size_scalefactor_ctx0 * tcp.window_size_scalefactor_ctx1)
tcp.len_ctx1 = (tcp.len_ctx0 + tcp.len_ctx2)
tcp.window_size_ctx2 != (tcp.window_size_scalefactor_ctx0 * tcp.window_size_value_ctx0)
ip.len_ctx0 = (ip.hdr_len_ctx1 + tcp.hdr_len_ctx0)
tcp.seq_ctx2 = (tcp.ack_ctx2 + tcp.seq_ctx0)
tcp.window_size_value_ctx1 != (tcp.window_size_scalefactor_ctx0 * tcp.window_size_value_ctx0)
ip.len_ctx0 != (ip.len_ctx2 + tcp.len_ctx0)
tcp.options.timestamp.tsval_ctx0 > tcp.options.timestamp.tsval_ctx1
tcp.hdr_len_ctx0 <= tcp.hdr_len_ctx2
ip.len_ctx1 > (ip.hdr_len_ctx0 + tcp.hdr_len_ctx0)
tcp.hdr_len_ctx1 = (ip.hdr_len_ctx0 + tcp.hdr_len_ctx0)
tcp.window_size_ctx2 > (tcp.window_size_scalefactor_ctx1 + tcp.window_size_ctx0)
tcp.len_ctx1 = (tcp.hdr_len_ctx1 + tcp.hdr_len_ctx2)
tcp.ack_ctx2 = (tcp.ack_ctx1 + tcp.seq_ctx1)
ip.len_ctx0 > (ip.hdr_len_ctx2 + tcp.hdr_len_ctx0)
tcp.flags_ctx0 = 17
tcp.window_size_value_ctx0 != tcp.window_size_ctx1
ip.len_ctx0 != (ip.hdr_len_ctx2 + tcp.hdr_len_ctx2)
tcp.hdr_len_ctx1 = (tcp.hdr_len_ctx2 + tcp.len_ctx2)
tcp.ack_ctx1 != (tcp.ack_ctx2 + tcp.seq_ctx1)
tcp.window_size_scalefactor_ctx0 != tcp.window_size_scalefactor_ctx1
tcp.options.timestamp.tsecr_ctx1 <= tcp.options.timestamp.tsecr_ctx2
ip.len_ctx2 > (ip.len_ctx0 + tcp.len_ctx2)
tcp.ack_ctx1 != (tcp.seq_ctx0 + tcp.seq_ctx2)
tcp.window_size_ctx1 > (tcp.window_size_scalefactor_ctx2 * tcp.window_size_value_ctx2)
ip.len_ctx2 > (tcp.hdr_len_ctx1 + tcp.len_ctx2)
tcp.window_size_ctx1 != (tcp.window_size_scalefactor_ctx0 * tcp.window_size_value_ctx1)
ip.len_ctx2 != (ip.len_ctx1 + tcp.len_ctx1)
tcp.len_ctx1 <= tcp.len_ctx2
ip.len_ctx2 > (ip.hdr_len_ctx1 + tcp.hdr_len_ctx0)
ip.len_ctx1 > ip.len_ctx2
ip.len_ctx1 > (ip.hdr_len_ctx1 + tcp.hdr_len_ctx1)
ip.len_ctx1 > (ip.len_ctx0 + tcp.len_ctx2)
tcp.window_size_value_ctx0 = (tcp.window_size_scalefactor_ctx1 * tcp.window_size_ctx1)
tcp.hdr_len_ctx0 != (tcp.hdr_len_ctx2 + tcp.len_ctx0)
tcp.window_size_ctx2 = (tcp.window_size_scalefactor_ctx2 * tcp.window_size_value_ctx1)
tcp.window_size_ctx2 > (tcp.window_size_scalefactor_ctx0 * tcp.window_size_ctx1)
ip.len_ctx1 > (ip.len_ctx2 + tcp.len_ctx0)
tcp.dstport_ctx0 = tcp.srcport_ctx2
tcp.window_size_ctx0 > (tcp.window_size_scalefactor_ctx0 * tcp.window_size_value_ctx2)
ip.len_ctx0 != (ip.len_ctx1 + tcp.len_ctx1)
tcp.dstport_ctx1 != tcp.srcport_ctx2
tcp.window_size_ctx0 <= (tcp.window_size_scalefactor_ctx0 * tcp.window_size_value_ctx1)
ip.hdr_len_ctx1 = (ip.hdr_len_ctx0 + tcp.len_ctx2)
tcp.window_size_value_ctx2 = (tcp.window_size_scalefactor_ctx1 + tcp.window_size_value_ctx1)
tcp.window_size_ctx0 != (tcp.window_size_scalefactor_ctx0 * tcp.window_size_value_ctx1)
tcp.seq_ctx0 != (tcp.ack_ctx0 + tcp.seq_ctx1)
ip.len_ctx0 != (ip.hdr_len_ctx1 + tcp.hdr_len_ctx0)
ip.ttl_ctx1 = ip.ttl_ctx2
ip.len_ctx2 <= (ip.hdr_len_ctx0 + tcp.hdr_len_ctx0)
ip.len_ctx0 <= (ip.hdr_len_ctx2 + tcp.hdr_len_ctx0)
tcp.hdr_len_ctx0 > (tcp.hdr_len_ctx2 + tcp.len_ctx0)
tcp.window_size_value_ctx2 > (tcp.window_size_scalefactor_ctx2 + tcp.window_size_value_ctx1)
tcp.window_size_ctx0 = tcp.window_size_ctx1
tcp.hdr_len_ctx1 != (tcp.hdr_len_ctx2 + tcp.len_ctx1)
tcp.seq_ctx2 != tcp.ack_ctx2
tcp.window_size_ctx2 <= (tcp.window_size_scalefactor_ctx0 * tcp.window_size_value_ctx1)
tcp.ack_ctx2 = (tcp.seq_ctx0 + tcp.seq_ctx1)
tcp.window_size_ctx0 != (tcp.window_size_scalefactor_ctx1 * tcp.window_size_value_ctx2)
tcp.window_size_ctx2 != (tcp.window_size_scalefactor_ctx0 * tcp.window_size_value_ctx1)
tcp.hdr_len_ctx0 > (tcp.hdr_len_ctx2 + tcp.len_ctx1)
ip.len_ctx1 != (ip.hdr_len_ctx0 + tcp.hdr_len_ctx2)
tcp.ack_ctx1 != (tcp.ack_ctx2 + tcp.seq_ctx0)
tcp.window_size_scalefactor_ctx1 != (tcp.window_size_scalefactor_ctx0 * tcp.window_size_scalefactor_ctx2)
ip.len_ctx0 = ip.len_ctx2
ip.len_ctx1 > (tcp.hdr_len_ctx2 + tcp.len_ctx1)
tcp.hdr_len_ctx0 = (ip.hdr_len_ctx0 + tcp.hdr_len_ctx1)
tcp.hdr_len_ctx2 = (ip.hdr_len_ctx1 + tcp.hdr_len_ctx1)
tcp.len_ctx0 != (tcp.hdr_len_ctx1 + tcp.hdr_len_ctx2)
tcp.len_ctx0 <= tcp.len_ctx2
tcp.options.timestamp.tsecr_ctx0 = tcp.options.timestamp.tsval_ctx2
tcp.window_size_ctx1 != (tcp.window_size_scalefactor_ctx0 * tcp.window_size_value_ctx0)
ip.len_ctx2 != (ip.len_ctx0 + tcp.len_ctx1)
ip.len_ctx1 != (ip.hdr_len_ctx2 + tcp.hdr_len_ctx2)
tcp.window_size_ctx1 <= (tcp.window_size_scalefactor_ctx0 + tcp.window_size_ctx0)
tcp.window_size_ctx2 > (tcp.window_size_scalefactor_ctx0 * tcp.window_size_value_ctx2)
tcp.window_size_ctx0 = tcp.window_size_value_ctx1
tcp.seq_ctx2 = (tcp.seq_ctx1 + 1)
tcp.window_size_ctx2 = (tcp.window_size_scalefactor_ctx2 + tcp.window_size_ctx1)
ip.len_ctx1 > (ip.hdr_len_ctx2 + tcp.hdr_len_ctx1)
tcp.len_ctx2 != (tcp.hdr_len_ctx0 + tcp.hdr_len_ctx1)
ip.src_ctx1 != ip.src_ctx2
tcp.ack_ctx1 != tcp.seq_ctx2
tcp.hdr_len_ctx0 != (tcp.hdr_len_ctx1 + tcp.len_ctx2)
ip.dst_ctx0 = ip.dst_ctx2
tcp.window_size_ctx1 > tcp.window_size_ctx2
tcp.len_ctx2 <= (tcp.hdr_len_ctx0 + tcp.hdr_len_ctx1)
ip.len_ctx1 = (ip.hdr_len_ctx0 + tcp.hdr_len_ctx0)
ip.len_ctx1 = (ip.hdr_len_ctx2 + tcp.hdr_len_ctx0)
tcp.window_size_ctx0 = (tcp.window_size_scalefactor_ctx0 * tcp.window_size_value_ctx1)
tcp.window_size_ctx2 != (tcp.window_size_scalefactor_ctx1 * tcp.window_size_value_ctx1)
tcp.window_size_value_ctx1 != (tcp.window_size_scalefactor_ctx0 * tcp.window_size_value_ctx2)
tcp.hdr_len_ctx0 = (tcp.hdr_len_ctx2 + tcp.len_ctx0)
tcp.window_size_ctx1 > (tcp.window_size_scalefactor_ctx0 * tcp.window_size_value_ctx1)
tcp.hdr_len_ctx1 <= (tcp.hdr_len_ctx0 + tcp.len_ctx1)
tcp.ack_ctx1 = (tcp.seq_ctx0 + tcp.seq_ctx2)
ip.len_ctx1 = (ip.hdr_len_ctx0 + tcp.hdr_len_ctx1)
ip.len_ctx0 > (ip.hdr_len_ctx2 + tcp.hdr_len_ctx2)
tcp.ack_ctx0 = tcp.seq_ctx1
ip.len_ctx2 > (ip.hdr_len_ctx1 + tcp.hdr_len_ctx2)
tcp.ack_ctx2 = (tcp.seq_ctx0 + 1)
ip.len_ctx2 = (ip.hdr_len_ctx1 + tcp.hdr_len_ctx2)
tcp.flags_ctx1 = tcp.flags_ctx2
tcp.hdr_len_ctx1 != (tcp.hdr_len_ctx2 + tcp.len_ctx2)
tcp.options.timestamp.tsecr_ctx0 > 0
tcp.window_size_scalefactor_ctx1 != tcp.window_size_scalefactor_ctx2
tcp.window_size_value_ctx2 <= (tcp.window_size_scalefactor_ctx1 + tcp.window_size_value_ctx1)
tcp.window_size_value_ctx1 = (tcp.window_size_scalefactor_ctx1 * tcp.window_size_ctx1)
tcp.len_ctx0 != (tcp.hdr_len_ctx0 + tcp.hdr_len_ctx2)
ip.hdr_len_ctx2 != (ip.hdr_len_ctx1 + tcp.len_ctx0)
ip.len_ctx1 > (ip.hdr_len_ctx0 + tcp.hdr_len_ctx2)
tcp.hdr_len_ctx0 != (tcp.hdr_len_ctx1 + tcp.len_ctx1)
ip.len_ctx0 != (ip.len_ctx2 + tcp.len_ctx1)
tcp.window_size_value_ctx0 != (tcp.window_size_scalefactor_ctx1 * tcp.window_size_value_ctx1)
ip.len_ctx2 != (ip.len_ctx0 + tcp.len_ctx0)
tcp.len_ctx2 > 0
tcp.ack_ctx0 <= 1
ip.len_ctx2 != (ip.hdr_len_ctx2 + tcp.hdr_len_ctx2)
ip.dst_ctx0 = ip.src_ctx2
ip.hdr_len_ctx1 != (ip.hdr_len_ctx2 + tcp.len_ctx1)
tcp.flags_ctx0 = tcp.flags_ctx2
tcp.window_size_value_ctx0 != (tcp.window_size_scalefactor_ctx0 * tcp.window_size_value_ctx1)
ip.len_ctx0 > (ip.hdr_len_ctx0 + tcp.hdr_len_ctx1)
tcp.seq_ctx0 = tcp.seq_ctx2
tcp.window_size_value_ctx0 > tcp.window_size_value_ctx1
tcp.hdr_len_ctx1 = (ip.hdr_len_ctx1 + tcp.hdr_len_ctx2)
ip.len_ctx0 != (ip.hdr_len_ctx0 + tcp.hdr_len_ctx0)
tcp.window_size_value_ctx1 = (tcp.window_size_scalefactor_ctx1 * tcp.window_size_value_ctx0)
tcp.flags_ctx1 != 16
tcp.window_size_ctx2 > (tcp.window_size_scalefactor_ctx2 * tcp.window_size_value_ctx1)
tcp.hdr_len_ctx0 = (tcp.hdr_len_ctx1 + tcp.len_ctx2)
ip.len_ctx1 = (ip.hdr_len_ctx1 + tcp.hdr_len_ctx0)
ip.dst_ctx0 = ip.dst_ctx1
tcp.ack_ctx1 = (tcp.seq_ctx1 + 1)
tcp.window_size_scalefactor_ctx0 = tcp.window_size_scalefactor_ctx1
tcp.hdr_len_ctx1 <= (tcp.hdr_len_ctx2 + tcp.len_ctx0)
tcp.ack_ctx1 != (tcp.seq_ctx0 + 1)
ip.hdr_len_ctx1 != (ip.hdr_len_ctx0 + tcp.len_ctx2)
tcp.window_size_value_ctx2 = (tcp.window_size_scalefactor_ctx2 + tcp.window_size_value_ctx1)
ip.dst_ctx1 = ip.src_ctx2
tcp.window_size_ctx2 > (tcp.window_size_scalefactor_ctx2 + tcp.window_size_ctx0)
ip.len_ctx0 != (ip.hdr_len_ctx0 + tcp.hdr_len_ctx1)
tcp.window_size_ctx0 <= (tcp.window_size_scalefactor_ctx1 * tcp.window_size_value_ctx2)
tcp.seq_ctx1 = (tcp.ack_ctx1 + tcp.seq_ctx0)
tcp.hdr_len_ctx0 != (ip.hdr_len_ctx1 + tcp.hdr_len_ctx1)
tcp.options.timestamp.tsval_ctx1 > tcp.options.timestamp.tsecr_ctx2
tcp.len_ctx0 = (tcp.len_ctx1 + tcp.len_ctx2)
tcp.window_size_ctx2 <= (tcp.window_size_scalefactor_ctx2 + tcp.window_size_ctx0)
tcp.len_ctx0 > tcp.len_ctx1
tcp.seq_ctx0 <= 1
tcp.window_size_ctx0 != (tcp.window_size_scalefactor_ctx0 * tcp.window_size_value_ctx2)
tcp.ack_ctx1 != (tcp.seq_ctx1 + 1)
ip.ttl_ctx0 <= ip.ttl_ctx1
tcp.len_ctx0 = tcp.len_ctx1
tcp.seq_ctx0 != tcp.seq_ctx2
ip.len_ctx0 > (ip.len_ctx2 + tcp.len_ctx0)
tcp.window_size_value_ctx2 != (tcp.window_size_scalefactor_ctx2 + tcp.window_size_value_ctx1)
tcp.hdr_len_ctx2 > (tcp.hdr_len_ctx0 + tcp.len_ctx1)
tcp.window_size_ctx0 = (tcp.window_size_scalefactor_ctx2 + tcp.window_size_ctx2)
tcp.options.timestamp.tsecr_ctx0 = tcp.options.timestamp.tsecr_ctx2
tcp.len_ctx1 > (tcp.hdr_len_ctx1 + tcp.hdr_len_ctx2)
tcp.options.timestamp.tsecr_ctx1 > tcp.options.timestamp.tsecr_ctx2
tcp.window_size_ctx0 > (tcp.window_size_scalefactor_ctx2 * tcp.window_size_value_ctx0)
tcp.options.timestamp.tsval_ctx0 = tcp.options.timestamp.tsval_ctx2
ip.len_ctx2 > (ip.hdr_len_ctx0 + tcp.hdr_len_ctx0)
ip.len_ctx1 = ip.len_ctx2
ip.len_ctx2 <= (ip.hdr_len_ctx1 + tcp.hdr_len_ctx2)
tcp.ack_ctx1 = (tcp.ack_ctx2 + tcp.seq_ctx1)
tcp.hdr_len_ctx0 > (tcp.hdr_len_ctx2 + tcp.len_ctx2)
ip.len_ctx2 != (tcp.hdr_len_ctx0 + tcp.hdr_len_ctx1)
ip.len_ctx1 > (ip.hdr_len_ctx1 + tcp.hdr_len_ctx0)
tcp.flags_ctx1 != 24
tcp.hdr_len_ctx1 <= (tcp.hdr_len_ctx0 + tcp.len_ctx2)
tcp.len_ctx0 != (tcp.hdr_len_ctx0 + tcp.hdr_len_ctx1)
tcp.flags_ctx1 = 18
ip.len_ctx0 = (ip.hdr_len_ctx0 + tcp.hdr_len_ctx1)
tcp.window_size_ctx1 = tcp.window_size_ctx2
tcp.ack_ctx1 != (tcp.seq_ctx0 + tcp.seq_ctx1)
tcp.seq_ctx0 = tcp.ack_ctx1
ip.src_ctx0 = ip.dst_ctx1
tcp.hdr_len_ctx2 != (tcp.hdr_len_ctx1 + tcp.len_ctx1)
ip.len_ctx0 > (ip.len_ctx1 + tcp.len_ctx1)
tcp.window_size_ctx2 > (tcp.window_size_scalefactor_ctx1 * tcp.window_size_value_ctx2)
ip.len_ctx1 > (ip.hdr_len_ctx2 + tcp.hdr_len_ctx2)
tcp.options.timestamp.tsecr_ctx0 > tcp.options.timestamp.tsecr_ctx1
tcp.window_size_ctx2 = (tcp.window_size_scalefactor_ctx0 * tcp.window_size_value_ctx0)
tcp.window_size_value_ctx0 <= (tcp.window_size_scalefactor_ctx0 * tcp.window_size_value_ctx1)
tcp.window_size_ctx1 > (tcp.window_size_scalefactor_ctx1 * tcp.window_size_value_ctx0)
ip.len_ctx2 > (ip.hdr_len_ctx2 + tcp.hdr_len_ctx1)
ip.len_ctx2 > (ip.hdr_len_ctx2 + tcp.hdr_len_ctx0)
tcp.hdr_len_ctx1 != (ip.hdr_len_ctx0 + tcp.hdr_len_ctx0)
tcp.len_ctx0 <= (tcp.len_ctx1 + tcp.len_ctx2)
ip.hdr_len_ctx0 > 0
tcp.options.timestamp.tsecr_ctx0 <= tcp.options.timestamp.tsval_ctx2
tcp.flags_ctx0 != 17
tcp.len_ctx0 > (tcp.len_ctx1 + tcp.len_ctx2)
ip.len_ctx0 = (ip.len_ctx1 + tcp.len_ctx1)
tcp.window_size_ctx2 != (tcp.window_size_scalefactor_ctx0 + tcp.window_size_ctx0)
tcp.hdr_len_ctx1 > (tcp.hdr_len_ctx0 + tcp.len_ctx1)
tcp.hdr_len_ctx0 = (ip.hdr_len_ctx2 + tcp.hdr_len_ctx1)
ip.dst_ctx0 != ip.src_ctx1
tcp.flags_ctx0 != tcp.flags_ctx2
tcp.dstport_ctx0 = tcp.dstport_ctx1
tcp.len_ctx2 > (tcp.hdr_len_ctx0 + tcp.hdr_len_ctx1)
ip.len_ctx1 != (tcp.hdr_len_ctx0 + tcp.len_ctx1)
ip.ttl_ctx0 <= ip.ttl_ctx2
tcp.window_size_value_ctx1 <= (tcp.window_size_scalefactor_ctx1 + tcp.window_size_value_ctx0)
tcp.window_size_ctx0 > (tcp.window_size_scalefactor_ctx1 * tcp.window_size_value_ctx0)
tcp.window_size_ctx1 > (tcp.window_size_scalefactor_ctx0 * tcp.window_size_value_ctx0)
ip.len_ctx2 = (ip.len_ctx0 + tcp.len_ctx1)
tcp.seq_ctx2 = (tcp.ack_ctx0 + tcp.ack_ctx1)
tcp.ack_ctx0 != (tcp.ack_ctx2 + tcp.seq_ctx0)
ip.src_ctx1 = ip.dst_ctx2
ip.len_ctx0 <= (ip.hdr_len_ctx1 + tcp.hdr_len_ctx1)
tcp.window_size_ctx1 <= (tcp.window_size_scalefactor_ctx0 * tcp.window_size_value_ctx0)
tcp.srcport_ctx0 = tcp.dstport_ctx2
ip.len_ctx0 = (ip.hdr_len_ctx0 + tcp.hdr_len_ctx0)
tcp.seq_ctx2 = (tcp.ack_ctx0 + tcp.ack_ctx2)
ip.ttl_ctx0 != ip.ttl_ctx2
tcp.window_size_ctx2 != (tcp.window_size_scalefactor_ctx2 * tcp.window_size_value_ctx1)
ip.len_ctx2 != (ip.hdr_len_ctx1 + tcp.hdr_len_ctx2)
ip.src_ctx0 = ip.src_ctx2
ip.len_ctx1 = (ip.len_ctx2 + tcp.len_ctx0)
tcp.window_size_ctx2 != (tcp.window_size_scalefactor_ctx0 * tcp.window_size_ctx1)
tcp.ack_ctx2 != (tcp.seq_ctx1 + tcp.seq_ctx2)
tcp.ack_ctx2 = (tcp.ack_ctx0 + tcp.seq_ctx0)
tcp.window_size_ctx1 = (tcp.window_size_scalefactor_ctx1 * tcp.window_size_value_ctx0)
ip.hdr_len_ctx1 = (ip.hdr_len_ctx0 + tcp.len_ctx1)
ip.ttl_ctx0 > ip.ttl_ctx2
ip.len_ctx0 > (ip.len_ctx1 + tcp.len_ctx0)
ip.src_ctx0 != ip.dst_ctx1
tcp.hdr_len_ctx0 <= (tcp.hdr_len_ctx1 + tcp.len_ctx1)
tcp.hdr_len_ctx1 = (ip.hdr_len_ctx1 + tcp.hdr_len_ctx0)
ip.dst_ctx1 != ip.src_ctx2
tcp.options.timestamp.tsecr_ctx2 <= (tcp.options.timestamp.tsecr_ctx0 + tcp.options.timestamp.tsval_ctx1)
tcp.window_size_ctx2 <= (tcp.window_size_scalefactor_ctx2 * tcp.window_size_value_ctx1)
tcp.ack_ctx1 = (tcp.ack_ctx0 + tcp.seq_ctx0)
ip.len_ctx1 != (ip.hdr_len_ctx2 + tcp.hdr_len_ctx0)
tcp.window_size_ctx1 <= (tcp.window_size_scalefactor_ctx0 * tcp.window_size_value_ctx1)
tcp.hdr_len_ctx1 != (tcp.hdr_len_ctx0 + tcp.len_ctx0)
tcp.len_ctx0 > (tcp.hdr_len_ctx0 + tcp.hdr_len_ctx2)
ip.len_ctx1 <= (ip.hdr_len_ctx2 + tcp.hdr_len_ctx0)
tcp.window_size_ctx2 = (tcp.window_size_scalefactor_ctx0 * tcp.window_size_value_ctx1)
tcp.window_size_ctx1 > (tcp.window_size_scalefactor_ctx0 * tcp.window_size_ctx0)
ip.len_ctx0 <= (ip.hdr_len_ctx2 + tcp.hdr_len_ctx1)
tcp.hdr_len_ctx1 != (ip.hdr_len_ctx2 + tcp.hdr_len_ctx2)
ip.len_ctx1 != (ip.hdr_len_ctx1 + tcp.hdr_len_ctx1)
tcp.ack_ctx1 > 1
ip.len_ctx1 <= ip.len_ctx2
tcp.window_size_scalefactor_ctx1 = tcp.window_size_scalefactor_ctx2
tcp.hdr_len_ctx2 != (tcp.hdr_len_ctx0 + tcp.len_ctx2)
ip.src_ctx0 != ip.src_ctx2
ip.len_ctx2 <= (ip.hdr_len_ctx2 + tcp.hdr_len_ctx1)
tcp.seq_ctx2 != (tcp.ack_ctx1 + tcp.seq_ctx0)
ip.len_ctx0 != (ip.hdr_len_ctx1 + tcp.hdr_len_ctx2)
tcp.hdr_len_ctx1 = (tcp.hdr_len_ctx0 + tcp.len_ctx0)
ip.len_ctx0 > (ip.len_ctx2 + tcp.len_ctx1)
tcp.options.timestamp.tsval_ctx1 = tcp.options.timestamp.tsval_ctx2
ip.len_ctx1 = (ip.hdr_len_ctx1 + tcp.hdr_len_ctx2)
tcp.flags_ctx0 != 16
tcp.ack_ctx0 != tcp.seq_ctx1
ip.len_ctx1 > (tcp.hdr_len_ctx0 + tcp.hdr_len_ctx2)
tcp.window_size_value_ctx0 = (tcp.window_size_scalefactor_ctx0 * tcp.window_size_ctx1)
ip.ttl_ctx1 <= ip.ttl_ctx2
ip.src_ctx0 != ip.src_ctx1
tcp.window_size_scalefactor_ctx0 != tcp.window_size_scalefactor_ctx2
ip.len_ctx1 != (ip.len_ctx0 + tcp.len_ctx0)
tcp.window_size_ctx1 <= (tcp.window_size_scalefactor_ctx2 * tcp.window_size_value_ctx2)
ip.len_ctx2 != (ip.hdr_len_ctx0 + tcp.hdr_len_ctx1)
tcp.ack_ctx0 = (tcp.ack_ctx2 + tcp.seq_ctx0)
tcp.window_size_ctx0 <= tcp.window_size_value_ctx1
ip.hdr_len_ctx1 = (ip.hdr_len_ctx2 + tcp.len_ctx1)
tcp.hdr_len_ctx1 != (ip.hdr_len_ctx0 + tcp.hdr_len_ctx2)
ip.len_ctx2 = (ip.len_ctx0 + tcp.len_ctx2)
ip.len_ctx1 <= (tcp.hdr_len_ctx0 + tcp.hdr_len_ctx2)
ip.len_ctx2 > (ip.len_ctx0 + tcp.len_ctx1)
tcp.window_size_scalefactor_ctx2 = (tcp.window_size_scalefactor_ctx0 * tcp.window_size_scalefactor_ctx1)
tcp.window_size_ctx1 = (tcp.window_size_scalefactor_ctx0 * tcp.window_size_ctx2)
ip.src_ctx0 = ip.src_ctx1
tcp.hdr_len_ctx0 > tcp.hdr_len_ctx1
ip.ttl_ctx1 != ip.ttl_ctx2
tcp.options.timestamp.tsecr_ctx1 != tcp.options.timestamp.tsecr_ctx2
ip.len_ctx1 <= (ip.hdr_len_ctx1 + tcp.hdr_len_ctx1)
tcp.len_ctx2 <= 0
tcp.window_size_ctx2 != (tcp.window_size_scalefactor_ctx2 + tcp.window_size_ctx0)
ip.len_ctx0 != (ip.hdr_len_ctx1 + tcp.hdr_len_ctx1)
tcp.window_size_value_ctx0 = (tcp.window_size_scalefactor_ctx0 * tcp.window_size_ctx0)
tcp.hdr_len_ctx1 != (ip.hdr_len_ctx1 + tcp.hdr_len_ctx0)
tcp.window_size_ctx0 != (tcp.window_size_scalefactor_ctx0 * tcp.window_size_ctx1)
ip.len_ctx1 <= (tcp.hdr_len_ctx2 + tcp.len_ctx1)
tcp.hdr_len_ctx1 <= tcp.hdr_len_ctx2
ip.len_ctx0 <= (ip.len_ctx2 + tcp.len_ctx1)
tcp.window_size_value_ctx0 <= tcp.window_size_value_ctx1
tcp.ack_ctx2 != (tcp.ack_ctx0 + tcp.ack_ctx1)
tcp.flags_ctx1 != 18
tcp.window_size_value_ctx1 = (tcp.window_size_scalefactor_ctx1 + tcp.window_size_value_ctx0)
ip.len_ctx1 > (ip.hdr_len_ctx2 + tcp.hdr_len_ctx0)
ip.len_ctx0 > ip.len_ctx1
ip.len_ctx2 != (ip.hdr_len_ctx0 + tcp.hdr_len_ctx0)
tcp.seq_ctx2 = (tcp.ack_ctx0 + tcp.seq_ctx0)
ip.len_ctx0 > (ip.hdr_len_ctx0 + tcp.hdr_len_ctx2)
tcp.ack_ctx2 != (tcp.ack_ctx0 + tcp.seq_ctx2)
tcp.hdr_len_ctx0 > (tcp.hdr_len_ctx1 + tcp.len_ctx1)
tcp.hdr_len_ctx2 != (tcp.hdr_len_ctx1 + tcp.len_ctx2)
tcp.window_size_scalefactor_ctx0 = tcp.window_size_scalefactor_ctx2
tcp.ack_ctx2 = (tcp.ack_ctx1 + tcp.seq_ctx0)
tcp.len_ctx0 <= (tcp.hdr_len_ctx1 + tcp.hdr_len_ctx2)
tcp.hdr_len_ctx1 <= 0
tcp.window_size_value_ctx0 != tcp.window_size_value_ctx2
ip.len_ctx1 > (ip.len_ctx2 + tcp.len_ctx2)
ip.len_ctx2 = (ip.len_ctx1 + tcp.len_ctx0)
tcp.hdr_len_ctx1 = (ip.hdr_len_ctx0 + tcp.hdr_len_ctx2)
tcp.window_size_ctx0 = (tcp.window_size_scalefactor_ctx2 * tcp.window_size_value_ctx0)
tcp.window_size_value_ctx0 = tcp.window_size_ctx0
ip.dst_ctx1 = ip.dst_ctx2
tcp.len_ctx2 = (tcp.hdr_len_ctx1 + tcp.hdr_len_ctx2)
tcp.len_ctx0 = tcp.len_ctx2
tcp.seq_ctx2 != (tcp.ack_ctx0 + tcp.seq_ctx0)
ip.len_ctx2 > (ip.len_ctx1 + tcp.len_ctx0)
tcp.options.timestamp.tsval_ctx1 > tcp.options.timestamp.tsval_ctx2
tcp.window_size_ctx0 > (tcp.window_size_scalefactor_ctx2 * tcp.window_size_value_ctx2)
ip.ttl_ctx0 = ip.ttl_ctx2
tcp.options.timestamp.tsval_ctx0 != tcp.options.timestamp.tsecr_ctx1
ip.len_ctx1 != (ip.hdr_len_ctx0 + tcp.hdr_len_ctx0)
tcp.hdr_len_ctx0 != (tcp.hdr_len_ctx2 + tcp.len_ctx2)
tcp.srcport_ctx0 = tcp.srcport_ctx2
ip.len_ctx0 != (ip.hdr_len_ctx0 + tcp.hdr_len_ctx2)
tcp.window_size_ctx2 = (tcp.window_size_scalefactor_ctx1 + tcp.window_size_ctx0)
tcp.window_size_value_ctx2 != (tcp.window_size_scalefactor_ctx1 + tcp.window_size_value_ctx1)
tcp.options.timestamp.tsval_ctx0 <= tcp.options.timestamp.tsval_ctx2
tcp.len_ctx1 <= (tcp.hdr_len_ctx0 + tcp.hdr_len_ctx2)
ip.len_ctx2 = (tcp.hdr_len_ctx1 + tcp.len_ctx0)
tcp.window_size_ctx0 = tcp.window_size_ctx2
ip.len_ctx0 = (tcp.hdr_len_ctx1 + tcp.hdr_len_ctx2)
ip.hdr_len_ctx0 != (ip.hdr_len_ctx1 + tcp.len_ctx2)
ip.len_ctx0 = (ip.len_ctx2 + tcp.len_ctx1)
ip.len_ctx1 != (ip.len_ctx2 + tcp.len_ctx0)
ip.hdr_len_ctx2 = (ip.hdr_len_ctx0 + tcp.len_ctx2)
tcp.ack_ctx0 != (tcp.seq_ctx0 + 1)
tcp.seq_ctx1 = (tcp.ack_ctx0 + tcp.seq_ctx0)
tcp.dstport_ctx0 != tcp.srcport_ctx1
tcp.options.timestamp.tsecr_ctx0 != tcp.options.timestamp.tsecr_ctx2
tcp.len_ctx1 = (tcp.hdr_len_ctx0 + tcp.hdr_len_ctx2)
tcp.flags_ctx0 = 18
tcp.srcport_ctx0 = tcp.dstport_ctx1
ip.len_ctx1 <= (ip.hdr_len_ctx0 + tcp.hdr_len_ctx0)
tcp.options.timestamp.tsval_ctx0 > tcp.options.timestamp.tsecr_ctx2
ip.len_ctx2 != (tcp.hdr_len_ctx1 + tcp.len_ctx0)
tcp.window_size_ctx2 <= (tcp.window_size_scalefactor_ctx2 + tcp.window_size_ctx1)
ip.hdr_len_ctx0 = (ip.hdr_len_ctx1 + tcp.len_ctx0)
tcp.seq_ctx1 != (tcp.ack_ctx1 + tcp.seq_ctx0)
ip.len_ctx0 > (tcp.hdr_len_ctx1 + tcp.hdr_len_ctx2)
tcp.options.timestamp.tsecr_ctx2 != (tcp.options.timestamp.tsecr_ctx0 + tcp.options.timestamp.tsval_ctx1)
tcp.options.timestamp.tsecr_ctx0 != tcp.options.timestamp.tsval_ctx2
tcp.hdr_len_ctx0 = (tcp.hdr_len_ctx2 + tcp.len_ctx2)
tcp.window_size_ctx0 != tcp.window_size_ctx2
tcp.hdr_len_ctx0 = (tcp.hdr_len_ctx1 + tcp.len_ctx1)
tcp.window_size_ctx0 = (tcp.window_size_scalefactor_ctx1 * tcp.window_size_value_ctx0)
tcp.options.timestamp.tsval_ctx0 != (tcp.options.timestamp.tsecr_ctx0 + tcp.options.timestamp.tsecr_ctx1)
tcp.seq_ctx0 = tcp.ack_ctx2
tcp.options.timestamp.tsval_ctx1 <= tcp.options.timestamp.tsval_ctx2
tcp.hdr_len_ctx2 = (ip.hdr_len_ctx2 + tcp.hdr_len_ctx1)
ip.len_ctx2 <= (ip.len_ctx0 + tcp.len_ctx2)
ip.hdr_len_ctx0 = (ip.hdr_len_ctx1 + tcp.len_ctx1)
ip.len_ctx1 != (ip.len_ctx2 + tcp.len_ctx1)
tcp.dstport_ctx1 = tcp.dstport_ctx2
tcp.seq_ctx1 = (tcp.seq_ctx0 + 1)
tcp.hdr_len_ctx2 <= (tcp.hdr_len_ctx0 + tcp.len_ctx0)
tcp.options.timestamp.tsval_ctx0 != tcp.options.timestamp.tsval_ctx1
tcp.options.timestamp.tsval_ctx1 != tcp.options.timestamp.tsval_ctx2
tcp.window_size_value_ctx0 = tcp.window_size_value_ctx2
tcp.window_size_value_ctx1 <= (tcp.window_size_scalefactor_ctx0 + tcp.window_size_value_ctx0)
tcp.options.timestamp.tsval_ctx1 = (tcp.options.timestamp.tsecr_ctx0 + tcp.options.timestamp.tsecr_ctx2)
tcp.len_ctx0 <= (tcp.hdr_len_ctx0 + tcp.hdr_len_ctx2)
ip.len_ctx2 > 0
ip.len_ctx2 != (ip.len_ctx1 + tcp.len_ctx0)
tcp.window_size_ctx1 != (tcp.window_size_scalefactor_ctx2 * tcp.window_size_value_ctx0)
tcp.window_size_ctx2 > (tcp.window_size_scalefactor_ctx0 * tcp.window_size_value_ctx0)
ip.len_ctx0 > (ip.len_ctx2 + tcp.len_ctx2)
tcp.hdr_len_ctx0 <= (tcp.hdr_len_ctx1 + tcp.len_ctx0)
tcp.window_size_ctx0 = (tcp.window_size_scalefactor_ctx1 * tcp.window_size_ctx1)
tcp.window_size_ctx0 = (tcp.window_size_scalefactor_ctx1 * tcp.window_size_value_ctx2)
ip.len_ctx0 <= 0
tcp.flags_ctx1 = 17
ip.hdr_len_ctx2 = (ip.hdr_len_ctx0 + tcp.len_ctx0)
ip.len_ctx2 != (ip.hdr_len_ctx2 + tcp.hdr_len_ctx0)
tcp.hdr_len_ctx1 > tcp.hdr_len_ctx2
tcp.window_size_ctx0 = (tcp.window_size_scalefactor_ctx2 * tcp.window_size_value_ctx2)
tcp.hdr_len_ctx0 = tcp.hdr_len_ctx1
tcp.options.timestamp.tsecr_ctx1 = (tcp.options.timestamp.tsecr_ctx0 + tcp.options.timestamp.tsval_ctx0)
tcp.len_ctx1 <= (tcp.hdr_len_ctx0 + tcp.hdr_len_ctx1)
ip.len_ctx1 = (ip.len_ctx0 + tcp.len_ctx2)
tcp.options.timestamp.tsval_ctx0 > (tcp.options.timestamp.tsecr_ctx0 + tcp.options.timestamp.tsecr_ctx1)
tcp.ack_ctx0 != (tcp.ack_ctx1 + tcp.seq_ctx0)
ip.len_ctx0 <= (tcp.hdr_len_ctx1 + tcp.hdr_len_ctx2)
tcp.seq_ctx0 = tcp.ack_ctx0
tcp.options.timestamp.tsval_ctx0 <= tcp.options.timestamp.tsecr_ctx1
tcp.hdr_len_ctx0 = (tcp.hdr_len_ctx1 + tcp.len_ctx0)
ip.len_ctx0 <= (ip.len_ctx1 + tcp.len_ctx1)
tcp.len_ctx1 <= (tcp.len_ctx0 + tcp.len_ctx2)
ip.len_ctx1 != (ip.hdr_len_ctx1 + tcp.hdr_len_ctx0)
tcp.options.timestamp.tsecr_ctx0 > tcp.options.timestamp.tsval_ctx1
tcp.window_size_ctx0 != tcp.window_size_value_ctx1
tcp.ack_ctx2 > 1
ip.len_ctx2 > (ip.hdr_len_ctx1 + tcp.hdr_len_ctx1)
tcp.len_ctx0 = (tcp.hdr_len_ctx0 + tcp.hdr_len_ctx1)
tcp.len_ctx2 <= (tcp.hdr_len_ctx0 + tcp.hdr_len_ctx2)
ip.len_ctx0 <= (ip.len_ctx2 + tcp.len_ctx2)
tcp.options.timestamp.tsval_ctx1 > (tcp.options.timestamp.tsecr_ctx0 + tcp.options.timestamp.tsecr_ctx2)
ip.len_ctx0 <= (ip.hdr_len_ctx1 + tcp.hdr_len_ctx0)
tcp.seq_ctx2 != (tcp.seq_ctx1 + 1)
tcp.hdr_len_ctx2 > (tcp.hdr_len_ctx1 + tcp.len_ctx2)
tcp.window_size_ctx0 <= (tcp.window_size_scalefactor_ctx2 * tcp.window_size_value_ctx1)
tcp.srcport_ctx1 != tcp.dstport_ctx2
ip.hdr_len_ctx1 != (ip.hdr_len_ctx2 + tcp.len_ctx0)
ip.hdr_len_ctx2 <= 0
ip.len_ctx0 > (ip.len_ctx1 + tcp.len_ctx2)
tcp.flags_ctx2 = 17
tcp.len_ctx2 = (tcp.hdr_len_ctx0 + tcp.hdr_len_ctx1)
ip.len_ctx0 = (ip.len_ctx2 + tcp.len_ctx0)
ip.len_ctx1 != (ip.len_ctx2 + tcp.len_ctx2)
tcp.options.timestamp.tsval_ctx1 != (tcp.options.timestamp.tsecr_ctx0 + tcp.options.timestamp.tsecr_ctx2)
ip.len_ctx2 <= (tcp.hdr_len_ctx1 + tcp.len_ctx0)
tcp.window_size_ctx1 != (tcp.window_size_scalefactor_ctx2 * tcp.window_size_value_ctx1)
tcp.window_size_value_ctx0 != (tcp.window_size_scalefactor_ctx1 * tcp.window_size_ctx0)
tcp.ack_ctx2 != (tcp.ack_ctx1 + tcp.seq_ctx0)
tcp.window_size_ctx1 = (tcp.window_size_scalefactor_ctx0 * tcp.window_size_ctx0)
ip.len_ctx2 <= (ip.hdr_len_ctx1 + tcp.hdr_len_ctx1)
tcp.window_size_value_ctx1 > (tcp.window_size_scalefactor_ctx0 * tcp.window_size_value_ctx2)
ip.len_ctx1 <= (ip.len_ctx0 + tcp.len_ctx2)
tcp.window_size_scalefactor_ctx1 > tcp.window_size_scalefactor_ctx2
tcp.window_size_value_ctx1 = (tcp.window_size_scalefactor_ctx0 * tcp.window_size_value_ctx2)
tcp.ack_ctx1 = (tcp.seq_ctx0 + 1)
ip.len_ctx2 = (ip.len_ctx1 + tcp.len_ctx2)
tcp.options.timestamp.tsecr_ctx0 <= tcp.options.timestamp.tsval_ctx1
tcp.options.timestamp.tsecr_ctx2 = (tcp.options.timestamp.tsecr_ctx0 + tcp.options.timestamp.tsval_ctx1)
tcp.seq_ctx1 != tcp.seq_ctx2
tcp.window_size_value_ctx0 = (tcp.window_size_scalefactor_ctx1 * tcp.window_size_ctx0)
tcp.window_size_ctx2 = (tcp.window_size_scalefactor_ctx0 + tcp.window_size_ctx0)
tcp.hdr_len_ctx1 != tcp.hdr_len_ctx2
tcp.hdr_len_ctx0 != tcp.hdr_len_ctx1
tcp.ack_ctx1 != (tcp.ack_ctx0 + tcp.seq_ctx0)
ip.len_ctx1 <= (ip.len_ctx2 + tcp.len_ctx1)
tcp.options.timestamp.tsval_ctx0 > tcp.options.timestamp.tsecr_ctx1
ip.len_ctx0 > ip.len_ctx2
tcp.len_ctx0 = (tcp.hdr_len_ctx1 + tcp.hdr_len_ctx2)
tcp.len_ctx2 <= (tcp.hdr_len_ctx1 + tcp.hdr_len_ctx2)
tcp.hdr_len_ctx0 != (ip.hdr_len_ctx2 + tcp.hdr_len_ctx1)
tcp.window_size_value_ctx1 = (tcp.window_size_scalefactor_ctx0 * tcp.window_size_value_ctx0)
tcp.window_size_ctx2 != (tcp.window_size_scalefactor_ctx0 * tcp.window_size_value_ctx2)
tcp.window_size_ctx1 = (tcp.window_size_scalefactor_ctx2 * tcp.window_size_value_ctx0)
tcp.hdr_len_ctx1 = (ip.hdr_len_ctx2 + tcp.hdr_len_ctx0)
ip.len_ctx0 > (tcp.hdr_len_ctx1 + tcp.len_ctx2)
tcp.hdr_len_ctx1 > (tcp.hdr_len_ctx2 + tcp.len_ctx0)
ip.len_ctx0 != ip.len_ctx2
tcp.hdr_len_ctx2 = (ip.hdr_len_ctx0 + tcp.hdr_len_ctx1)
ip.len_ctx0 <= (ip.hdr_len_ctx0 + tcp.hdr_len_ctx0)
tcp.window_size_ctx1 != (tcp.window_size_scalefactor_ctx1 * tcp.window_size_value_ctx0)
ip.hdr_len_ctx1 != (ip.hdr_len_ctx2 + tcp.len_ctx2)
tcp.hdr_len_ctx1 != (ip.hdr_len_ctx1 + tcp.hdr_len_ctx2)
tcp.seq_ctx2 != (tcp.ack_ctx2 + tcp.seq_ctx0)
tcp.seq_ctx1 <= 1
tcp.flags_ctx2 = 24
tcp.ack_ctx2 = (tcp.ack_ctx0 + tcp.ack_ctx1)
tcp.hdr_len_ctx0 != tcp.hdr_len_ctx2
ip.len_ctx0 > (ip.hdr_len_ctx1 + tcp.hdr_len_ctx1)
tcp.window_size_ctx0 <= tcp.window_size_ctx2
tcp.ack_ctx0 = tcp.ack_ctx2
ip.dst_ctx1 != ip.dst_ctx2
tcp.len_ctx1 > (tcp.hdr_len_ctx0 + tcp.hdr_len_ctx1)
ip.dst_ctx0 = ip.src_ctx1
tcp.window_size_value_ctx1 = (tcp.window_size_scalefactor_ctx0 + tcp.window_size_value_ctx0)
ip.hdr_len_ctx1 = (ip.hdr_len_ctx0 + tcp.len_ctx0)
tcp.window_size_ctx1 != (tcp.window_size_scalefactor_ctx0 + tcp.window_size_ctx0)
tcp.hdr_len_ctx2 = (tcp.hdr_len_ctx0 + tcp.len_ctx0)
ip.len_ctx1 > 0
tcp.ack_ctx2 != (tcp.ack_ctx0 + tcp.seq_ctx0)
tcp.len_ctx1 <= 0
tcp.len_ctx1 != (tcp.hdr_len_ctx0 + tcp.hdr_len_ctx1)
tcp.window_size_ctx0 > (tcp.window_size_scalefactor_ctx2 + tcp.window_size_ctx2)
ip.len_ctx2 != (ip.hdr_len_ctx0 + tcp.hdr_len_ctx2)
ip.len_ctx2 <= (ip.len_ctx1 + tcp.len_ctx1)
tcp.hdr_len_ctx1 = (tcp.hdr_len_ctx0 + tcp.len_ctx1)
tcp.flags_ctx2 != 16
ip.len_ctx0 != (ip.len_ctx2 + tcp.len_ctx2)
tcp.options.timestamp.tsval_ctx1 <= tcp.options.timestamp.tsecr_ctx2
ip.len_ctx2 != (ip.hdr_len_ctx2 + tcp.hdr_len_ctx1)
tcp.window_size_ctx0 = (tcp.window_size_scalefactor_ctx0 * tcp.window_size_ctx1)
tcp.window_size_scalefactor_ctx2 <= (tcp.window_size_scalefactor_ctx0 * tcp.window_size_scalefactor_ctx1)
tcp.window_size_ctx0 <= (tcp.window_size_scalefactor_ctx0 + tcp.window_size_ctx2)
tcp.ack_ctx0 != tcp.ack_ctx1
tcp.ack_ctx0 = tcp.seq_ctx2
tcp.hdr_len_ctx0 != (tcp.hdr_len_ctx1 + tcp.len_ctx0)
