# Copyright (c) 2020 ETH Zurich
#
# SPDX-License-Identifier: BSL-1.0
# Distributed under the Boost Software License, Version 1.0. (See accompanying
# file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

#configure_extra_options+=" -DLCI_DEBUG=ON"
configure_extra_options+=" -DFETCHCONTENT_SOURCE_DIR_LCI=${LCI_SOURCE_PATH}"

# The pwrapi library still needs to be set up properly on rostam
# configure_extra_options+=" -DHPX_WITH_POWER_COUNTER=ON"
